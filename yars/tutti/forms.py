from django import forms
from tutti.models import Review, Booking
from tutti.models import UserProfile

numOfPeopleChoices = (
    ("1", "One"),
    ("2", "Two"),
    ("3", "Three"),
    ("4", "Four"),
    ("5", "Five"),
    ("6", "Six"),
)

class numPeopleForm(forms.ModelForm):
    numofPeople = forms.ChoiceField(choices = numOfPeopleChoices)


# class dateTimeForm(forms.Modelform):

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('phoneNum', 'address', 'gender',)
    