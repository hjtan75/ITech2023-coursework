from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from tutti.models import Review, Booking, UserProfile
from django.template.defaultfilters import register


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


def reviews(request):
    if request.method == 'POST':
        if request.user.is_authenticated:
            try:
                user = UserProfile.objects.filter(user__username=request.user.username).first()
                rating = int(request.POST.get('rating', 0))
                description = request.POST.get('description')
                review = Review(user=user, rating=rating, description=description)
                review.save()
                html = '''<div class="layui-col-md6 layui-col-md-offset3">
                <fieldset class="layui-elem-field">
                <legend>''' + review.user.user.username
                for i in range(5):
                    if i < int(review.rating):
                        html += '''<i class="layui-icon layui-icon-star-fill" style="color:orange"></i>'''
                    else:
                        html += '''<i class="layui-icon layui-icon-star" style="color:orange"></i>'''
                html += '''
                </legend>
                <div class="layui-field-box" style="text-align: justify;">
                    ''' + review.description + '''
                </div>
            </fieldset>
        </div>'''
                return JsonResponse({"success": True, "msg": "Added successfully.", 'html': html})
            except Exception as e:
                return JsonResponse({"success": False, "msg": "Failed to add."})
        else:
            return JsonResponse({"success": False, "msg": "Please login first."})
    reviews_ = Review.objects.all()
    return render(request, 'tutti/review.html', context={'reviews': reviews_})

@register.filter
def range_(value):
    return range(value)
