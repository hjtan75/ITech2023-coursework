from django.urls import path
from tutti import views

app_name = 'tutti'

urlpatterns = [
    path('', views.index, name='index'),
    path('register_profile/', views.register_profile, name='register_profile'),
    path('profile/<username>/', views.ProfileView.as_view(), name='profile'),
    path('profiles/', views.ListProfilesView.as_view(), name='list_profiles'),
    path('show_bookings/', views.show_bookings, name='show_bookings'),
    path('delete_booking/', views.DeleteBookingView.as_view(), name='delete_booking'),
    path('edit_booking/', views.EditBookingView.as_view(), name='edit_booking'),
    path('booking/', views.booking, name='booking'),
    path('booking/date-and-time', views.booking_date_and_time, name='booking_date_time'),
    path('booking/confirmation', views.booking_confirmation, name='booking_confirmation'),
    path('booking/completed', views.booking_completed, name='booking_completed'),
    path('menu/', views.booking_completed, name='booking_completed'),
    path('reviews/', views.reviews, name='reviews'),



]