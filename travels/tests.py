from django.test import TestCase
from travels.models import Trip, TripReservation, TripDates
from biuropodrozy.outer_api.covid_api import get_covid
from biuropodrozy.outer_api.weather_api import get_weather
from biuropodrozy.outer_api.exchange_rates_api import get_rate_in_pln
from travels.forms import TripReservationForm
from django.contrib.auth import get_user_model
import datetime


class TripTestCase(TestCase):
    def setUp(self):
        Trip.objects.create(title="Hotel Tobbaco",country="Polska",city="Łódź", countryEN="Poland", currency="PLN",
                            timezone="UTC+1", landscape=5, type=1, transport=2, price=1000, duration=2)

    def test_trip_covid_api(self):
        """"""
        trip = Trip.objects.get(title="Hotel Tobbaco")
        res_covid_api = get_covid("Poland")
        self.assertDictEqual(trip.covid_api, res_covid_api)

    def test_trip_weather_api(self):
        """"""
        trip = Trip.objects.get(title="Hotel Tobbaco")
        res_weather_api = get_weather("Poland")
        self.assertDictEqual(trip.weather_api, res_weather_api)

    def test_trip_exchange_rates_api(self):
        """"""
        trip = Trip.objects.get(title="Hotel Tobbaco")
        res_exchange_rates_api = get_rate_in_pln("PLN")
        self.assertDictEqual(trip.exchange_rates_api, res_exchange_rates_api)

    def test_get_absolute_url(self):
        trip = Trip.objects.get(title="Hotel Tobbaco")
        self.assertEqual(trip.get_absolute_url(), '/oferty/hotel-tobbaco/')

    def test_trip__str__(self):
        trip = Trip.objects.get(title="Hotel Tobbaco")
        self.assertEqual(str(trip), 'Hotel Tobbaco 2dni')

    def test_adding_trip_date(self):
        """"""
        trip = Trip.objects.get(title="Hotel Tobbaco")
        tripdate = TripDates.objects.create(trip=trip, start_date=datetime.date(2021, 6, 21))
        expected_end_date = datetime.date(2021, 6, 23)
        self.assertEquals(tripdate.end_date, expected_end_date)


class TripReservationTest(TestCase):

    def test_form_is_valid(self):
        Trip.objects.create(title="Hotel Tobbaco", country="Polska", city="Łódź", countryEN="Poland", currency="PLN",
                            timezone="UTC+1", landscape=5, type=1, transport=2, price=1000, duration=2)
        trip = Trip.objects.get(title="Hotel Tobbaco")
        tripdate = TripDates.objects.create(trip=trip, start_date=datetime.date.today())
        user = get_user_model().objects.create_user('john', 'lennon@thebeatles.com', 'johnpassword')
        reservation = TripReservation.objects.create(user=user,
                                                     trip=trip,
                                                     date=tripdate,
                                                     persons=2,
                                                     phone="123456789",
                                                     guide=False,
                                                     room=False,
                                                     all_inclusive=False,
                                                     price=1000
                                                     )
        form = TripReservationForm(data={'user':reservation.user,
                                         'trip':reservation.trip,
                                         'date':reservation.date,
                                         'persons': reservation.persons,
                                         'phone': reservation.phone,
                                         'guide': reservation.guide,
                                         'room': reservation.room,
                                         'all_inclusive': reservation.all_inclusive,
                                         })
        self.assertTrue(form.is_valid())

