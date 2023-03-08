from django import forms
from tutti.models import Review, Booking

numOfPeopleChoices =(
    ("1", "One"),
    ("2", "Two"),
    ("3", "Three"),
    ("4", "Four"),
    ("5", "Five"),
    ("6", "Six"),
)

class numPeopleForm(forms.Modelform):
    numofPeople = forms.ChoiceField(numOfPeopleChoices)

class dateTimeForm(forms.Modelform):
    