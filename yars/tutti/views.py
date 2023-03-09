from django.shortcuts import render
from django.http import HttpResponse
from django.utils.decorators import method_decorator
from django.views import View
from django.contrib.auth.decorators import login_required
from tutti.models import User, Booking
from django.http import JsonResponse
import tutti.booking_function

# Create your views here.
def index(request):
    return HttpResponse("Rango says hey there partner!")


# View to show booking
def show_bookings(request):
    # Create a context dictionary which we can pass
    # to the template rendering engine.
    context_dict = {}
    try:
        # Can we find a booking with the given username?
        # If we can't, the .get() method raises a DoesNotExist exception.
        # The .get() method returns one model instance or raises an exception.
        bookings = Booking.objects.filter(user_id=8)
        print(bookings[0].time)
        print(bookings[0].date)
        print(bookings[1].time)
        print(bookings[1].date)
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


# View to delete booking.
class DeleteBookingView(View):

    def get(self, request):
        booking_id = request.GET['booking_id']
        try:
            bookings = Booking.objects.get(bookingID=booking_id)
            print(bookings)
        except bookings.DoesNotExist:
            return HttpResponse(-1)
        except ValueError:
            return HttpResponse(-1)
        bookings.delete()

        return JsonResponse({'status': 'success'})


class EditBookingView(View):

    def get(self, request):
        booking_id = request.GET['booking_id']
        numOFPeople = request.GET['numberOFPeople']
        date = request.GET['date']
        time = request.GET['time']
        notes = request.GET['notes']
        seat = tutti.booking_function.numSeatsForDate(date)
        print("seat num")
        print(seat)
        try:
            bookings = Booking.objects.get(bookingID=booking_id)
            #print(bookings)
        except bookings.DoesNotExist:
            return HttpResponse(-1)
        except ValueError:
            return HttpResponse(-1)
        bookings.numberOfPeople = numOFPeople
        bookings.date = date
        bookings.time = time
        bookings.notes = notes
        bookings.save()

        return JsonResponse({'status': 'success'})


def booking(request):
    context_dict = {}
    context_dict['numOfPeoples'] = [1, 2, 3, 4, 5, 6]

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


