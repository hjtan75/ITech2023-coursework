from django.urls import path
from tutti import views

app_name = 'tutti'

urlpatterns = [
    path('', views.index, name='index'),
    path('show_bookings/', views.show_bookings, name='show_bookings'),
    path('booking/', views.booking, name='booking'),
    path('booking/date-and-time', views.booking_date_and_time, name='booking_date_time'),
]