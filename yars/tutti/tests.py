from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from tutti.models import Review, User, Booking, UserProfile
import json
from datetime import date


# helper function to create test user and user profile
def create_test_user():
    user = User.objects.create_user(
        username='testuser',
        email='testuser@example.com',
        password='password123'
    )
    user_profile = UserProfile.objects.create(
        user=user,
        phoneNum='Test phone',
        address='Test location',
        gender='M'
    )
    return user, user_profile


# helper function to create test booking
def create_test_booking(user_profile):
    booking = Booking.objects.create(
        user=user_profile,
        date='2023-03-21',
        time='12:00',
        numberOfPeople=4,
        notes='Test notes',
        bookingStatus=True
    )
    return booking


# UserProfile Test
class UserProfileTestCase(TestCase):
    def setUp(self):
        # Create a user and its userprofile
        self.user, self.user_profile = create_test_user()

    def test_user_profile(self):
        """
           Test user profile.
        """
        user_profile = UserProfile.objects.get(user__username='testuser')
        self.assertEqual(user_profile.phoneNum, 'Test phone')
        self.assertEqual(user_profile.address, 'Test location')
        self.assertEqual(user_profile.gender, 'M')


# BookingView Test
class ShowBookingsTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user, self.user_profile = create_test_user()
        self.booking = create_test_booking(user_profile=self.user_profile)

    def test_show_bookings_authenticated(self):
        """
            Test if bookings can be showed correctly.
        """
        self.client.login(username='testuser', password='password123')
        response = self.client.get('/tutti/show_bookings/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Your Reservations')
        self.assertContains(response, 'BookingID')
        self.assertContains(response, 'Date')
        self.assertContains(response, 'Time')
        self.assertContains(response, 'Number of People')
        self.assertContains(response, 'Description')
        self.assertContains(response, 'Edit')
        self.assertContains(response, 'Delete')
        self.assertContains(response, self.booking.bookingID)
        self.assertContains(response, self.booking.date)
        self.assertContains(response, self.booking.time)
        self.assertContains(response, self.booking.numberOfPeople)
        self.assertContains(response, self.booking.notes)

    def test_show_booking_view_with_no_bookings(self):
        """
        If no booking exist, the appropriate message should be displayed.
        """
        user = User.objects.create_user(
            username='testuser2',
            email='testuser2@example.com',
            password='password123'
        )
        self.client.login(username='testuser2', password='password123')
        response = self.client.get(reverse('tutti:show_bookings'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'No bookings currently.')
        self.assertQuerysetEqual(response.context['bookings'], [])

# Review test
class ReviewsTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user, self.user_profile = create_test_user()

    def test_reviews_post(self):
        """
            Test to post review.
        """
        self.client.login(username='testuser', password='password123')
        response = self.client.post('/tutti/reviews/', {
            'rating': 5,
            'description': 'Test review'
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Review.objects.count(), 1)
        self.assertEqual(Review.objects.first().user, self.user_profile)
        self.assertEqual(Review.objects.first().rating, 5)
        self.assertEqual(Review.objects.first().description, 'Test review')

    def test_reviews_post_not_authenticated(self):
        """
            Test if user is not authenticated, the app would redirect user to login
        """
        response = self.client.post('/tutti/reviews/', {
            'rating': 5,
            'description': 'Test review'
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/accounts/login/?next=/tutti/reviews/')


# Test delete booking
class DeleteBookingViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user, self.user_profile = create_test_user()
        self.booking = create_test_booking(user_profile=self.user_profile)

    def test_delete_booking(self):
        """
             Test delete booking
        """
        self.client.login(username='testuser', password='password123')
        response = self.client.get(reverse('tutti:delete_booking'), {'booking_id': self.booking.bookingID})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.content), {'status': 'success'})
        self.assertRaises(Booking.DoesNotExist, Booking.objects.get, bookingID=self.booking.bookingID)


# Test edit booking
class EditBookingViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.client = Client()
        self.user, self.user_profile = create_test_user()
        self.booking = create_test_booking(user_profile=self.user_profile)

    def test_edit_booking_success(self):
        """
            Test edit booking
        """
        self.client.login(username='testuser', password='password123')
        response = self.client.get(reverse('tutti:edit_booking'), {
            'booking_id': self.booking.bookingID,
            'numberOFPeople': 3,
            'date': '2023-03-22',
            'time': '12:30',
            'notes': 'New notes'
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.content), {'status': 'success'})
        self.booking.refresh_from_db()
        self.assertEqual(self.booking.numberOfPeople, 3)
        self.assertEqual(str(self.booking.date), '2023-03-22')
        self.assertEqual(self.booking.time, '12:30')
        self.assertEqual(self.booking.notes, 'New notes')

    def test_edit_booking_fail(self):
        """
            Test if edit failed, it would not change the booking
        """
        self.client.login(username='testuser', password='password123')
        response = self.client.get(reverse('tutti:edit_booking'), {
            'booking_id': self.booking.bookingID,
            'numberOFPeople': 36,
            'date': '2023-03-22',
            'time': '12:30',
            'notes': 'New notes'
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.content), {'status': 'fail'})
        self.booking.refresh_from_db()
        self.assertEqual(self.booking.numberOfPeople, 4)
        self.assertEqual(str(self.booking.date), '2023-03-21')
        self.assertEqual(self.booking.time, '12:00')
        self.assertEqual(self.booking.notes, 'Test notes')







