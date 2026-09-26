from django.shortcuts import render, redirect
from .models import Emenitites, Movie, Actor, Booking, Showtime
from django.http import JsonResponse
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.utils import timezone


def home(request):
    emenities = Emenitites.objects.all()
    context = {'emenities': emenities}
    return render(request, 'home.html', context)


def api_movies(request):
    movies_objs = Movie.objects.all()

    price = request.GET.get('price')
    if price:
        movies_objs = movies_objs.filter(price__lte=price)

    emenities = request.GET.get('emenities')
    if emenities:
        emenities = [int(e) for e in emenities.split(',') if e.isdigit()]
        movies_objs = movies_objs.filter(emenities__in=emenities).distinct()

    payload = [{'id': movie_obj.id,
                'movie_name': movie_obj.movie_name,
                'movie_description': movie_obj.movie_description,
                'movie_image': movie_obj.movie_image,
                'price': movie_obj.price} for movie_obj in movies_objs]

    return JsonResponse(payload, safe=False)


def movie_detail(request, movie_id):
    movie_obj = Movie.objects.get(id=movie_id)
    payload = {
        'id': movie_obj.id,
        'movie_name': movie_obj.movie_name,
        'movie_description': movie_obj.movie_description,
        'movie_image': movie_obj.movie_image,
        'price': movie_obj.price,
        'actors': [{'name': a.name, 'photo': a.photo} for a in movie_obj.actors.all()],
    }
    return JsonResponse(payload)


def showtimes_api(request, movie_id):
    movie_obj = Movie.objects.get(id=movie_id)
    showtimes = movie_obj.showtimes.filter(date_time__gte=timezone.now()).order_by('date_time')
    payload = [{
        'id': s.id,
        'date_time': s.date_time.strftime('%d %b, %I:%M %p'),
        'seats_left': s.seats_left(),
    } for s in showtimes]
    return JsonResponse(payload, safe=False)


def seat_map_api(request, showtime_id):
    showtime_obj = Showtime.objects.get(id=showtime_id)
    payload = {
        'total_seats': showtime_obj.movie.total_seats,
        'booked_seats': showtime_obj.booked_seat_list(),
        'price': showtime_obj.movie.price,
    }
    return JsonResponse(payload)


@login_required(login_url='login')
def book_ticket(request, showtime_id):
    if request.method == "POST":
        showtime_obj = Showtime.objects.get(id=showtime_id)
        seat_numbers = request.POST.get('seat_numbers', '')
        seats_requested = [s for s in seat_numbers.split(',') if s.strip().isdigit()]

        if not seats_requested:
            messages.error(request, "Please select at least one seat.")
            return redirect('/')

        already_booked = showtime_obj.booked_seat_list()
        conflict = [s for s in seats_requested if int(s) in already_booked]
        if conflict:
            messages.error(request, "Some selected seats were just taken. Please pick again.")
            return redirect('/')

        total = showtime_obj.movie.price * len(seats_requested)

        Booking.objects.create(
            user=request.user,
            showtime=showtime_obj,
            seat_numbers=seat_numbers,
            total_price=total
        )

        new_booked = already_booked + [int(s) for s in seats_requested]
        showtime_obj.booked_seats = ','.join(str(s) for s in new_booked)
        showtime_obj.save()

        messages.success(request, f"Booked seats {seat_numbers}! Total: ${total}")
        return redirect('my_bookings')

    return redirect('/')


@login_required(login_url='login')
def my_bookings(request):
    bookings = Booking.objects.filter(user=request.user).order_by('-booked_at')
    return render(request, 'my_bookings.html', {'bookings': bookings})


def login_page(request):
    if request.method == "POST":
        try:
            username = request.POST.get('username')
            password = request.POST.get('password')
            user_obj = User.objects.filter(username=username)

            if not user_obj.exists():
                messages.error(request, "Username not found")
                return redirect('/login/')

            user_obj = authenticate(username=username, password=password)

            if user_obj:
                login(request, user_obj)
                return redirect('/')

            messages.error(request, "Wrong Password")
            return redirect('/login/')

        except Exception as e:
            messages.error(request, "Something went wrong")
            return redirect('/login/')

    return render(request, "login.html")


def register_page(request):
    if request.method == "POST":
        try:
            username = request.POST.get('username')
            password = request.POST.get('password')
            user_obj = User.objects.filter(username=username)

            if user_obj.exists():
                messages.error(request, "Username is taken")
                return redirect('/register/')

            user_obj = User.objects.create(username=username)
            user_obj.set_password(password)
            user_obj.save()

            messages.success(request, "Account created")
            return redirect('/login/')

        except Exception as e:
            messages.error(request, "Something went wrong")
            return redirect('/register/')

    return render(request, "register.html")


def custom_logout(request):
    logout(request)
    return redirect('login')