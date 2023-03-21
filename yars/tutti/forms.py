from django import forms
from tutti.models import Review, Booking
from tutti.models import UserProfile, User
from datetime import datetime, date

numOfPeopleChoices = (
    ("1", "1"),
    ("2", "2"),
    ("3", "3"),
    ("4", "4"),
    ("5", "5"),
    ("6", "6"),
)

# Function to create predefined timeslots for booking
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

class BookingDateForm(forms.Form):
    date = forms.DateField(widget=forms.SelectDateWidget(empty_label=("Choose Year", "Choose Month", "Choose Day"),
                                                         years=(2023, 2024)))

    # def __init__(self):
    #     self.date
    
    

class BookingTimeForm(forms.Form):
    timeSlots = createTimeSlotsTuple()
    time = forms.ChoiceField(choices=timeSlots, required=True)
    notes = forms.CharField(max_length=1000, required=False) 


class numPeopleForm(forms.Form):
    numberOfPeople = forms.ChoiceField(label="Number of people",choices=numOfPeopleChoices) 


# class BookingConfirmationForm(forms.ModelForm):
    # timeSlots = createTimeSlotsTuple()
    # date  = forms.DateField(widget=forms.HiddenInput(), initial=datetime.now().date())
    # time = forms.ChoiceField(widget=forms.HiddenInput(), choices=timeSlots, initial=timeSlots[0])
    # numOfPeople = forms.IntegerField(widget=forms.HiddenInput(), initial=1)
    # notes = forms.CharField(widget=forms.HiddenInput(), max_length=1000, initial="", required=False)
    # bookingStatus = forms.BooleanField(widget=forms.HiddenInput(), initial=True)

    # class Meta:
    #     model = Booking
    #     fields = ()


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('phoneNum', 'address', 'gender',)
    