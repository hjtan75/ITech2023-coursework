import os
import random
from datetime import datetime
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'yars.settings')


import django
django.setup()
from tutti.models import User, Booking

numOfPeoplePerSlow = 30

def numSeatsForDate(date_string):
    # Return the number of seats left for a given date
    # Date is string with format yy-mm-dd
    dt = datetime.strptime(date_string, '%Y-%m-%d').date()
    booking = Booking.objects.filter(date=dt)
    print(booking)


# def dateForNumSeats(num):
#     # Return which date is available for that number of seats

if __name__ == "__main__":
    numSeatsForDate("2023-03-03")