import os
import random
from datetime import datetime
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'yars.settings')


import django
from django.db.models import Sum, Count
django.setup()
from tutti.models import User, Booking

numOfPeoplePerSlot = 30

def createTimeSlotsTuple():
    startHour = 12
    endHour = 24

    timeslots = []
    for hour in range(startHour, endHour+1):
        for minute in range(0, 31, 30):
            if hour != endHour or minute != 30:
                hourString = str(hour)
                minString = str(minute) if minute == 30 else str(minute) + "0"
                timeslots.append((f"{hourString}:{minString}", f"{hourString}:{minString}"))

    return tuple(timeslots)

def timeSlotsTupleToList(time_slot_tuple):
    time_slot_list = []
    for time_slot_tuple_element in time_slot_tuple:
        time_slot_list.append(time_slot_tuple_element[0])

    return time_slot_list


def numSeatsForDate(date_string, time_string):
    # Return the number of seats left for a given date
    # Date is string with format yyyy-mm-dd
    # Time is string with format HH:mm
    dt = datetime.strptime(date_string, '%Y-%m-%d').date()
    nop = Booking.objects.filter(date=dt, time=time_string).aggregate(Sum('numberOfPeople'))

    seats_left = 30

    if nop["numberOfPeople__sum"] != None:
        seats_left = numOfPeoplePerSlot - nop["numberOfPeople__sum"]

    return seats_left


def timeForNumSeatsAndDate(numSeatRequested, date_obj):
    # Return which date and time is available for that number of seats
    timeUnavailable = []
    timeAvailable = []
    timeSlots = createTimeSlotsTuple()
    timeSlots = timeSlotsTupleToList(timeSlots)

    results = (Booking.objects
               .filter(bookingStatus=True, 
                       date__year=date_obj.strftime("%Y"),
                       date__month=date_obj.strftime("%m"),
                       date__day=date_obj.strftime("%d"))
               .values('time')
               .annotate(dcount=Sum('numberOfPeople'))
               .order_by('time'))

    for result in results:
        if numOfPeoplePerSlot - result['dcount'] < numSeatRequested:
            time = result['time']
            timeUnavailable.append(time)

    for timeSlot in timeSlots:
        if timeSlot not in timeUnavailable:
            timeAvailable.append(timeSlot)

    return timeAvailable



if __name__ == "__main__":
    dt = datetime(2023, 1, 1).date()
    # print(dt)
    print(timeForNumSeatsAndDate(6, dt))