from django.shortcuts import render, redirect
from django.http import HttpResponse
from tutti.models import User, Booking
from tutti.forms import numPeopleForm
# Create your views here.
def index(request):
    return HttpResponse("Rango says hey there partner!")


def show_bookings(request):
    # Create a context dictionary which we can pass
    # to the template rendering engine.
    context_dict = {}
    try:
        # Can we find a booking with the given username?
        # If we can't, the .get() method raises a DoesNotExist exception.
        # The .get() method returns one model instance or raises an exception.
        bookings = Booking.objects.filter(user_id=1)
        print(bookings)
        # Retrieve all of the associated bookings.
        # Adds our results list to the template context under name pages.
        context_dict['bookings'] = bookings

    except Booking.DoesNotExist:
        # We get here if we didn't find the specified booking.
        # Don't do anything -
        # the template will display the "no category" message for us.
        context_dict['bookings'] = None

    # Go render the response and return it to the client.
    return render(request, 'tutti/show_bookings.html', context=context_dict)


def booking(request):
    context_dict = {}

    form = numPeopleForm()
    context_dict['form'] = form

    # if request.method == 'POST':
    #     form = numPeopleForm(request.POST)

    # if form.is_valid():
    #     # Save the new category and return to index page
    #     print(form)
    #     return redirect('tutti/booking_date_time.html')
    # else:
    #     print(form.errors)

    # Loading the form
    print(form)
    return render(request, 'tutti/booking_num_people.html', context=context_dict)

def booking_date_and_time(request):
    context_dict = {}
    context_dict['months'] = ['June', 'July', 'August', 'September']
    context_dict['days'] = ['01', '02', '05', '06']
    context_dict['times'] = ['0500', '0900', '1230', '1500']

    return render(request, 'tutti/booking_date_time.html', context=context_dict)


def booking_confirmation(request):
    context_dict = {}
    context_dict['user'] = 'Adam Smith'
    context_dict['phone'] = '07465898556'
    context_dict['email'] = 'testing@testing.com'
    context_dict['datatime'] = '19:30 26 February 2022'
    context_dict['numOfPeoples'] = 5

    return render(request, 'tutti/booking_confirmation.html', context=context_dict)

def booking_completed(request):
    return render(request, 'tutti/booking_completed.html')

