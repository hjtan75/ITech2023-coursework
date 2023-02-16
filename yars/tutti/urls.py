from django.urls import path
from tutti import views

app_name = 'tutti'

urlpatterns = [
    path('', views.index, name='index'),
    path('show_bookings/', views.show_bookings, name='show_bookings'),


]