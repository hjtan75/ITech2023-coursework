from django.db import models
from django.contrib.auth.models import User


def createTimeSlotsTuple():
    # Function to create predefined timeslots for booking
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

class UserProfile(models.Model):
    # Store the information about a user
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phoneNum =  models.CharField(max_length=14)
    address = models.CharField(max_length=128)
    gender = models.CharField(max_length=1)

    def __str__(self):
        return self.user.username

class Booking(models.Model):
    # Store booking information
    # bookingStatus: true = expired booking, false = pending booking

    timeSlots = createTimeSlotsTuple()
    bookingID = models.AutoField(primary_key=True)
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    date = models.DateField()
    time = models.CharField(max_length=5, choices=timeSlots, default=timeSlots[0])
    numberOfPeople = models.IntegerField()
    notes = models.CharField(max_length=1000, blank=True)
    bookingStatus = models.BooleanField()

    def __str__(self):
        return str(self.bookingID)
    

class Review(models.Model):
    # Store the reviews made by 
    
    reviewID = models.AutoField(primary_key=True)
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    rating = models.IntegerField()
    description = models.CharField(max_length=1000)

    def __str__(self):
        return str(self.reviewID)
    
class Category(models.Model):
    # Create a Category model to represent the categories of the menu

    name = models.CharField(max_length=50)
    background_image = models.ImageField(upload_to='category_backgrounds/')
    def __str__(self):
        return self.name


class MenuSpecific(models.Model):
    #Create a MenuSpecific model to represent specific dishes in the menu

    name = models.CharField(max_length=50)
    description = models.TextField()
    price = models.DecimalField(max_digits=5, decimal_places=1)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return self.name