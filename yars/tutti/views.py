from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.utils.decorators import method_decorator
from django.views import View
from django.contrib.auth.decorators import login_required
from tutti.models import User, Booking, UserProfile
from tutti.forms import  UserProfileForm
from django.http import JsonResponse
import tutti.booking_function
from tutti.forms import numPeopleForm

from tutti.models import Review, User, Booking
from django.template.defaultfilters import register

from django.urls import reverse

# Create your views here.
def index(request):

    context_dict = {}
    context_dict['boldmessage'] = 'Crunchy, creamy, cookie, candy, cupcake!'
    # Return response back to the user, updating any cookies that need changed.
    return render(request, 'tutti/index.html', context=context_dict)


@login_required
def register_profile(request):
    form = UserProfileForm()
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES)
        if form.is_valid():
            user_profile = form.save(commit=False)
            user_profile.user = request.user
            user_profile.save()
            return redirect(reverse('tutti:index'))
        else:
            print(form.errors)
    context_dict = {'form': form}
    return render(request, 'tutti/profile_registration.html', context_dict)


class ProfileView(View):
    def get_user_details(self, username):
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return None

        user_profile = UserProfile.objects.get_or_create(user=user)[0]
        form = UserProfileForm({'phoneNum': user_profile.phoneNum,
                                'address': user_profile.address,
                                'gender': user_profile.gender})

        return user, user_profile, form

    @method_decorator(login_required)
    def get(self, request, username):
        try:
            (user, user_profile, form) = self.get_user_details(username)
        except TypeError:
            return redirect(reverse('tutti:index'))

        context_dict = {'user_profile': user_profile,
                        'selected_user': user,
                        'form': form}

        return render(request, 'tutti/profile.html', context_dict)

    @method_decorator(login_required)
    def post(self, request, username):
        try:
            (user, user_profile, form) = self.get_user_details(username)
        except TypeError:
            return redirect(reverse('tutti:index'))

        form = UserProfileForm(request.POST, request.FILES, instance=user_profile)

        if form.is_valid():
            form.save(commit=True)
            return redirect(reverse('tutti:profile',
                                    kwargs={'username': username}))
        else:
            print(form.errors)

        context_dict = {'user_profile': user_profile,
                        'selected_user': user,
                        'form': form}

        return render(request, 'tutti/profile.html', context_dict)


class ListProfilesView(View):
    @method_decorator(login_required)
    def get(self, request):
        profiles = UserProfile.objects.all()

        return render(request, 'tutti/list_profiles.html', {'user_profile_list': profiles})


# View to show booking
def show_bookings(request):
    # Create a context dictionary which we can pass
    # to the template rendering engine.
    context_dict = {}
    try:
        # Can we find a booking with the given username?
        # If we can't, the .get() method raises a DoesNotExist exception.
        # The .get() method returns one model instance or raises an exception.
        bookings = Booking.objects.filter(user_id=9)
        # print(bookings[0].time)
        # print(bookings[0].date)
        # Retrieve all of the associated bookings.
        # Adds our results list to the template context under name pages.
        context_dict['bookings'] = bookings

    except Booking.DoesNotExist:
        # We get here if we didn't find the specified booking.
        # Don't do anything -
        # the template will display the "no category" message for us.
        context_dict['bookings'] = None

    # Go render the response and return it to the client.
    return render(request, 'tutti/your_booking.html', context=context_dict)


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
        numOFPeople = int(request.GET['numberOFPeople'])
        date = request.GET['date']
        time = request.GET['time']
        # print(time)
        notes = request.GET['notes']
        seats_left = tutti.booking_function.numSeatsForDate(date, time)
        # print("seat num")
        # print(seat)
        try:
            bookings = Booking.objects.get(bookingID=booking_id)

        except bookings.DoesNotExist:
            return HttpResponse(-1)
        except ValueError:
            return HttpResponse(-1)
        if seats_left >= numOFPeople:
            bookings.numberOfPeople = numOFPeople
            bookings.date = date
            bookings.time = time
            bookings.notes = notes
            bookings.save()
            return JsonResponse({'status': 'success'})
        else:
            return JsonResponse({'status': 'fail'})



# def booking(request):
#     context_dict = {}

#     form = numPeopleForm()
#     context_dict['form'] = form

#     # if request.method == 'POST':
#     #     form = numPeopleForm(request.POST)

#     # if form.is_valid():
#     #     # Save the new category and return to index page
#     #     print(form)
#     #     return redirect('tutti/booking_date_time.html')
#     # else:
#     #     print(form.errors)

#     # Loading the form
#     print(form)
#     return render(request, 'tutti/booking_num_people.html', context=context_dict)


def booking_date_and_time(request):
    context_dict = {}
    context_dict['months'] = ['June', 'July', 'August', 'September']
    context_dict['days'] = ['01', '02', '05', '06']
    context_dict['times'] = ['0500', '0900', '1230', '1500']

#     return render(request, 'tutti/booking_date_time.html', context=context_dict)


# def booking_confirmation(request):
#     context_dict = {}
#     context_dict['user'] = 'Adam Smith'
#     context_dict['phone'] = '07465898556'
#     context_dict['email'] = 'testing@testing.com'
#     context_dict['datatime'] = '19:30 26 February 2022'
#     context_dict['numOfPeoples'] = 5

#     return render(request, 'tutti/booking_confirmation.html', context=context_dict)

def booking_completed(request):
    return render(request, 'tutti/booking_completed.html')



def reviews(request):
    if request.method == 'POST':
        ...
    # reviews_ = Review.objects.filter(user_id=1)
    reviews_ = Review.objects.all()
    return render(request, 'tutti/review.html', context={'reviews': reviews_})

@register.filter
def range_(value):
    return range(value)

