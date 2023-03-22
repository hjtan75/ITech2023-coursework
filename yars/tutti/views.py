from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.utils.decorators import method_decorator
from django.views import View
from django.contrib.auth.decorators import login_required
from tutti.models import User, Booking, UserProfile
from tutti.forms import  UserProfileForm, BookingDateForm, numPeopleForm, BookingTimeForm #, BookingConfirmationForm
from django.http import JsonResponse
import tutti.booking_function
from datetime import datetime, date
# from tutti.forms import numPeopleForm
from django.views.decorators.csrf import csrf_exempt
from tutti.models import Review, User, Booking, Category, MenuSpecific
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
        current_user = UserProfile.objects.filter(user=request.user).first()
        bookings = Booking.objects.filter(user=current_user)

        # Retrieve all of the associated bookings.
        # Adds our results list to the template context under name pages.
        context_dict['bookings'] = bookings

    except Booking.DoesNotExist:
        # We get here if we didn't find the specified booking.
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


@login_required
def booking_num_people(request):
    context_dict = {}

    if request.method == 'POST':
        booking_form = numPeopleForm(request.POST)

        if booking_form.is_valid():
            numOfPeople = booking_form.cleaned_data['numberOfPeople']
            request.session['numOfPeople'] = numOfPeople
            return redirect(reverse('tutti:booking_date'))
    else:
        booking_form = numPeopleForm()
        
    context_dict['form'] = booking_form
    return render(request, 'tutti/booking_num_people.html', context=context_dict)



@login_required
def booking_date(request):
    context_dict = {}
    
    if request.method == 'POST':
        booking_form = BookingDateForm(request.POST)

        if booking_form.is_valid():
            # checking there are empty slots for the given time
            date_obj = booking_form.cleaned_data['date']
            numOfPeople = request.session['numOfPeople']
            time_available = tutti.booking_function.timeForNumSeatsAndDate(int(numOfPeople), date_obj)
            
            if len(time_available) != 0:
                request.session['chosen_date'] = date_obj.strftime('%d/%m/%Y')
                request.session['time_list'] = time_available
                return redirect(reverse('tutti:booking_time'))
            else:
                return HttpResponse('Not available for that date')
    else:
        booking_form = BookingDateForm()

    context_dict['form'] = booking_form
    return render(request, 'tutti/booking_date.html', context=context_dict)


@login_required
def booking_time(request):
    context_dict = {}
    available_time_list = request.session['time_list']
    
    if request.method == 'POST':
        booking_form = BookingTimeForm(request.POST)

        if booking_form.is_valid():
            chosen_time = booking_form.cleaned_data['time']
            notes = booking_form.cleaned_data['notes']

            if chosen_time in available_time_list:
                request.session['chosen_time'] = chosen_time
                request.session['notes'] = notes
                return redirect(reverse('tutti:booking_confirmation'))
            else:
                return HttpResponse('Not available for that time')
    else:
        booking_form = BookingTimeForm()
        booking_form.fields['time'].choices = [(available_time, available_time) for available_time in available_time_list]

    context_dict['form'] = booking_form
    return render(request, 'tutti/booking_time.html', context=context_dict)


@login_required
def booking_confirmation(request):
    context_dict = {}
    # Extract information from session request
    current_user = UserProfile.objects.filter(user=request.user).first()
    chosen_time = request.session['chosen_time']
    numOfPeople = request.session['numOfPeople']
    chosen_date_obj = datetime.strptime(request.session['chosen_date'], '%d/%m/%Y').date()
    notes = request.session['notes']

    # Add booking information to context dict 
    context_dict['chosen_time'] = chosen_time
    context_dict['numOfPeople'] = numOfPeople
    context_dict['chosen_date'] = datetime.strftime(chosen_date_obj, '%d/%m/%Y')
    context_dict['user_name'] = str(current_user)
    context_dict['user_email'] = current_user.user.email
    context_dict['user_phone_number'] = current_user.phoneNum
    context_dict['user_address'] = current_user.address
    context_dict['notes'] = notes
    return render(request, 'tutti/booking_confirmation.html', context=context_dict)

@login_required
def booking_completed(request):
    context_dict = {}
    # Extract information from session request
    current_user = UserProfile.objects.filter(user=request.user).first()
    chosen_time = request.session['chosen_time']
    numOfPeople = request.session['numOfPeople']
    chosen_date_obj = datetime.strptime(request.session['chosen_date'], '%d/%m/%Y').date()
    notes = request.session['notes']

    booking = Booking(user=current_user, date=chosen_date_obj, time=chosen_time, 
                      numberOfPeople=numOfPeople, notes=notes, bookingStatus=True)
    # Clear session
    booking.save()
    # request.session['chosen_time'] = None
    # request.session['numOfPeople'] = None

    return render(request, 'tutti/booking_completed.html')


@csrf_exempt
@login_required
def reviews(request):
    if request.method == 'POST':
        if request.user.is_authenticated:
            try:
                user = UserProfile.objects.filter(user__username=request.user.username).first()
                rating = int(request.POST.get('rating', 0))
                description = request.POST.get('description')
                review = Review(user=user, rating=rating, description=description)
                review.save()
                return JsonResponse({"status": True, "msg": "Added successfully."})
            except Exception as e:
                return JsonResponse({"status": False, "msg": "Failed to add."})
        else:
            return JsonResponse({"status": False, "msg": "Please login first."})
    reviews_ = Review.objects.all()
    return render(request, 'tutti/review.html', context={'reviews': reviews_})


@register.filter
def range_(value):
    return range(value)

# Define menu view functions to handle requests for menu pages
def menu(request):
    categories = Category.objects.all()
    menu_specific = MenuSpecific.objects.all()
    context = {'categories': categories, 'menu_specific': menu_specific}
    return render(request, 'tutti/menu.html', context)

# Define the about view function to handle requests about our page
def about(request):
    return render(request, 'tutti/about_page.html')
