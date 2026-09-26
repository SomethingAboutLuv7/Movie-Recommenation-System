from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login_page, name='login'),
    path('register/', views.register_page, name='register'),
    path('logout/', views.custom_logout, name='logout'),
    path('api/movies', views.api_movies, name='api_movies'),
    path('api/movies/<int:movie_id>/', views.movie_detail, name='movie_detail'),
    path('api/movies/<int:movie_id>/showtimes/', views.showtimes_api, name='showtimes_api'),
    path('api/showtimes/<int:showtime_id>/seats/', views.seat_map_api, name='seat_map_api'),
    path('book/<int:showtime_id>/', views.book_ticket, name='book_ticket'),
    path('my-bookings/', views.my_bookings, name='my_bookings'),
]