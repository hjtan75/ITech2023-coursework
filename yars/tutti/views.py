from django.shortcuts import render
from django.http import HttpResponse
from tutti.models import User, Booking
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
