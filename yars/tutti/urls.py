from django.urls import path
from tutti import views

app_name = 'tutti'

# Routing rule that map URL to views.

urlpatterns = [
    path('', views.index, name='index'),
    path('register_profile/', views.register_profile, name='register_profile'),
    path('profile/<username>/', views.ProfileView.as_view(), name='profile'),
    path('profiles/', views.ListProfilesView.as_view(), name='list_profiles'),
    path('show_bookings/', views.show_bookings, name='show_bookings'),
    path('delete_booking/', views.DeleteBookingView.as_view(), name='delete_booking'),
    path('edit_booking/', views.EditBookingView.as_view(), name='edit_booking'),
    path('booking_num_people/', views.booking_num_people, name='booking_num_people'),
    path('booking_date/', views.booking_date, name='booking_date'),
    path('booking_time/', views.booking_time, name='booking_time'),
    path('booking_confirmation/', views.booking_confirmation, name='booking_confirmation'),
    path('booking_completed/', views.booking_completed, name='booking_completed'),
    path('reviews/', views.reviews, name='reviews'),
    path('about/', views.about, name='about'),
    path('menu/', views.menu, name='menu'),
]