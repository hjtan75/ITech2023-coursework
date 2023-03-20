from django.contrib import admin
from tutti.models import UserProfile, Booking, Review
# Register your models here.

class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'phoneNum', 'address', 'gender')

class BookingAdmin(admin.ModelAdmin):
    list_display = ('bookingID', 'user', 'date', 'time', 'numberOfPeople', 'bookingStatus')

class ReviewAdmin(admin.ModelAdmin):
    list_display = ('reviewID', 'user', 'rating')


admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(Booking, BookingAdmin)
admin.site.register(Review, ReviewAdmin)




