import os
import random
from datetime import datetime
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'yars.settings')


import django
from django.db.models import Sum
django.setup()
from tutti.models import User, Booking

numOfPeoplePerSlot = 30

def numSeatsForDate(date_string):
    # Return the number of seats left for a given date
    # Date is string with format yy-mm-dd
    dt = datetime.strptime(date_string, '%Y-%m-%d').date()
    nop = Booking.objects.filter(date=dt).aggregate(Sum('numberOfPeople'))
    seats_left = numOfPeoplePerSlot - nop["numberOfPeople__sum"]
    return seats_left

# def dateForNumSeats(num):
#     # Return which date is available for that number of seats

if __name__ == "__main__":
    numSeatsForDate("2023-01-06")