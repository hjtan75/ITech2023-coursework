from django.urls import path
from tutti import views

app_name = 'tutti'

urlpatterns = [
    path('', views.index, name='index'),
    path('show_bookings/', views.show_bookings, name='show_bookings'),
    path('reviews/', views.reviews, name='reviews'),
    path('booking/', views.booking, name='booking'),
    path('booking/date-and-time', views.booking_date_and_time, name='booking_date_time'),
    path('booking/confirmation', views.booking_confirmation, name='booking_confirmation'),
    path('booking/completed', views.booking_completed, name='booking_completed'),
    path('menu/', views.booking_completed, name='booking_completed'),

]