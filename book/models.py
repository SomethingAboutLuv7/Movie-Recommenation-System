from django.db import models
from django.contrib.auth.models import User

class Emenitites(models.Model):
    name = models.CharField(max_length=100)
    def __str__(self):
        return self.name


class Actor(models.Model):
    name = models.CharField(max_length=100)
    photo = models.CharField(max_length=500)
    bio = models.TextField(blank=True)

    def __str__(self):
        return self.name


class Movie(models.Model):
    movie_name = models.CharField(max_length=100)
    movie_description = models.TextField()
    movie_image = models.CharField(max_length=500)
    price = models.IntegerField()
    total_seats = models.IntegerField(default=50)
    emenities = models.ManyToManyField(Emenitites)
    actors = models.ManyToManyField(Actor, blank=True)

    def __str__(self):
        return self.movie_name


class Showtime(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='showtimes')
    date_time = models.DateTimeField()
    booked_seats = models.CharField(max_length=1000, blank=True, default='')

    def __str__(self):
        return f"{self.movie.movie_name} - {self.date_time.strftime('%d %b, %I:%M %p')}"

    def booked_seat_list(self):
        return [int(s) for s in self.booked_seats.split(',') if s.strip().isdigit()]

    def seats_left(self):
        return self.movie.total_seats - len(self.booked_seat_list())


class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    showtime = models.ForeignKey(Showtime, on_delete=models.CASCADE)
    seat_numbers = models.CharField(max_length=500)
    total_price = models.IntegerField()
    booked_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.showtime} ({self.seat_numbers})"