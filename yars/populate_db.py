import os
import random
from faker import Faker
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'yars.settings')


import django
django.setup()
from tutti.models import UserProfile, Booking, Review
from django.contrib.auth.models import User, UserManager

def populate():
    user_IDs = []
    faker = Faker()

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
            booking_date = faker.date()
            booking_numberOfPeople = random.randint(1,6)
            booking_notes = faker.text(max_nb_chars=1000)
            booking_bookingStatus = random.choice([True, False])
            add_booking(userProfileObj, booking_date, booking_numberOfPeople, booking_notes, booking_bookingStatus)
            # print(f'Booking: {booking_date} | {booking_numberOfPeople} | {booking_notes} | {booking_bookingStatus}')

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

def add_booking(usr, dt, nop, note, bs):
    bookingObj = Booking.objects.get_or_create(user=usr, date=dt, numberOfPeople=nop, notes=note, bookingStatus=bs)[0]
    bookingObj.save()

def add_review(usr, rt, des):
    reviewObj = Review.objects.get_or_create(user=usr, rating=rt, description=des)[0]
    reviewObj.save()


if __name__ ==  '__main__':
    print('Starting tuitti population script...')
    populate()
