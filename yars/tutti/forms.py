from django import forms
from tutti.models import Review, Booking, UserProfile
from django.contrib.auth.models import User

numOfPeopleChoices = (
    ("1", "One"),
    ("2", "Two"),
    ("3", "Three"),
    ("4", "Four"),
    ("5", "Five"),
    ("6", "Six"),
)

# class BookingForm(forms.ModelForm):
#     numberOfPeople = forms.ChoiceField(choices = numOfPeopleChoices) 
#     notes = forms.CharField(max_length=1000)

#     # bookingID = 
#     # user = 
#     date = forms.DateField()
#     # time = 
#     numberOfPeople = forms.ChoiceField(choices = numOfPeopleChoices) 
#     notes = forms.CharField(max_length=1000)
#     # bookingStatus = 

#     class Meta:
#         model = Booking,



# class dateTimeForm(forms.Modelform):


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'email', 'password',)


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('phoneNum', 'address', 'gender',)
    