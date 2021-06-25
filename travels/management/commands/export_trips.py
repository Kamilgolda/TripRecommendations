import pandas as pd
from django.core.management.base import BaseCommand, CommandError
from travels.models import Trip, TripReservation


class Command(BaseCommand):
    """
    Tworzenie pól dla wycieczki, eksportwoanie wycieczek do exela
    """
    help = "Creating fields in Trips"

    trips = Trip.objects.all()
    reservations = TripReservation.objects.all().order_by('trip')
    trips_dict = {"title": [],
                  "hotelstars": [],
                  "rating": [],
                  "country": [],
                  "city": [],
                  "currency": [],
                  "timezone": [],
                  "climate": [],
                  "landscape": [],
                  "type": [],
                  "transport": [],
                  "price": [],
                  "duration": []
                  }
    reservations_dict = {'user': [],
                         'trip': [],
                         'date': [],
                         'persons': [],
                         'phone': [],
                         'guide': [],
                         'room': [],
                         'all_inclusive': [],
                         'price': []
                         }

    full_path = 'travels/management/files/export_trips.xlsx'

    def handle(self, *args, **options):
        """
        Metoda zwraca wycieczki do pliku exela
        Args:
            *args ():
            **options ():

        Returns:
            object: plik exela z wycieczkami
        """
        for trip in self.trips:
            self.trips_dict["title"].append(trip.title)
            self.trips_dict["hotelstars"].append(trip.hotelstars)
            self.trips_dict["rating"].append(trip.rating)
            self.trips_dict["country"].append(trip.country)
            self.trips_dict["city"].append(trip.city)
            self.trips_dict["currency"].append(trip.currency)
            self.trips_dict["timezone"].append(trip.timezone)
            self.trips_dict["climate"].append(trip.climate)
            self.trips_dict["landscape"].append(trip.landscape)
            self.trips_dict["type"].append(trip.type)
            self.trips_dict["transport"].append(trip.transport)
            self.trips_dict["price"].append(trip.price)
            self.trips_dict["duration"].append(trip.duration)

        df1 = pd.DataFrame(self.trips_dict,
                           columns=['title', 'hotelstars', 'rating', 'country', 'city', 'currency', 'timezone',
                                    'climate', 'landscape', 'type', 'transport', 'price', 'duration'])

        for reservation in self.reservations:
            self.reservations_dict["user"].append(reservation.user)
            self.reservations_dict["trip"].append(reservation.trip)
            self.reservations_dict["date"].append(reservation.date)
            self.reservations_dict["persons"].append(reservation.persons)
            self.reservations_dict["phone"].append(reservation.phone)
            self.reservations_dict["guide"].append(reservation.guide)
            self.reservations_dict["room"].append(reservation.room)
            self.reservations_dict["all_inclusive"].append(reservation.all_inclusive)
            self.reservations_dict["price"].append(reservation.price)

        df2 = pd.DataFrame(self.reservations_dict,
                           columns=['user', 'trip', 'date', 'persons', 'phone', 'guide', 'room',
                                    'all_inclusive', 'price'])

        with pd.ExcelWriter(self.full_path) as writer:
            df1.to_excel(writer, sheet_name='Wycieczki')
            df2.to_excel(writer, sheet_name='Rezerwacje')
