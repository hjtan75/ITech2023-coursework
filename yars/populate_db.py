import os
import random
from datetime import datetime
from faker import Faker
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'yars.settings')


import django
django.setup()
from tutti.models import UserProfile, Booking, Review
from django.contrib.auth.models import User, UserManager

def populate():
    faker = Faker()
    timeSlots = createTimeSlotsTuple()

    for _ in range(50):
        userName = faker.name()
        userPassword = 'yars'
        userEmail = faker.email()
        phoneNum = faker.bothify('+##-###########')
        address = faker.address()
        gender = random.choice(['M', 'L'])
        
        # userObj = UserManager.create(username=userName, email=userEmail, password=userPassword)
        userObj = User.objects.create_user(username=userName, email=userEmail, password=userPassword)

        userObj.set_password = userPassword
        userObj.save()
        userProfileObj = add_userProfile(userObj, phoneNum, address, gender)
        # print(f'User: {userName} | {userPassword} | {userEmail} |{phoneNum} | {address} | {gender}')

        for _ in range(random.randint(0,5)):
            start_dt = datetime.strptime('2023-01-01', '%Y-%m-%d').date()
            end_dt = datetime.strptime('2023-03-08', '%Y-%m-%d').date()
            booking_date = faker.date_between(start_dt, end_dt)
            booking_time = random.choice(timeSlots)[0]
            booking_numberOfPeople = random.randint(1,6)
            booking_notes = faker.text(max_nb_chars=1000)
            booking_bookingStatus = random.choice([True, False])
            add_booking(userProfileObj, booking_date, booking_time, booking_numberOfPeople, booking_notes, booking_bookingStatus)
            # print(f'Booking: {booking_date} | {booking_time} | {booking_numberOfPeople} | {booking_notes} | {booking_bookingStatus}')

        for _ in range(random.randint(0,2)):
            review_rating = random.randint(1, 5)
            review_description = faker.text(max_nb_chars=1000)
            add_review(userProfileObj, review_rating, review_description)
        #     print(f'Review: {review_rating} | {review_description}')
        # print('-----------------------------------------------')
    
def add_userProfile(userObj, ph, addr, gen):
    userProfileObj = UserProfile.objects.get_or_create(user=userObj, phoneNum=ph, address=addr, gender=gen)[0]
    userProfileObj.save()
    return userProfileObj

def add_booking(usr, dt, tm, nop, note, bs):
    bookingObj = Booking.objects.get_or_create(user=usr, date=dt, time=tm, numberOfPeople=nop, notes=note, bookingStatus=bs)[0]
    bookingObj.save()

def add_review(usr, rt, des):
    reviewObj = Review.objects.get_or_create(user=usr, rating=rt, description=des)[0]
    reviewObj.save()

def createTimeSlotsTuple():
    startHour = 12
    endHour = 20

    timeslots = []
    for hour in range(startHour, endHour+1):
        for minute in range(0, 31, 30):
            if hour != endHour or minute != 30:
                hourString = str(hour)
                minString = str(minute) if minute == 30 else str(minute) + "0"
                timeslots.append((f"{hourString}:{minString}", f"{hourString}:{minString}"))

    return tuple(timeslots)


if __name__ ==  '__main__':
    print('Starting tuitti population script...')
    populate()
