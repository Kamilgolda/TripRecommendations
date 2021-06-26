import pandas as pd
import os.path
from django.core.management.base import BaseCommand, CommandError
from travels.models import TripReservation, Trip, TripDates
from django.contrib.auth import get_user_model
from biuropodrozy.users.models import User
import logging
import decimal
import numpy

class Command(BaseCommand):
    """
    Importowanie rezerwacji wycieczek ze sciezki:  travels/management/files/export_trips.xlsx
    """
    help = "Importing trip reservations from travels/management/files/export_trips.xlsx"

    full_path = 'travels/management/files/export_trips.xlsx'
    reservations = pd.read_excel(full_path, sheet_name="Rezerwacje")
    trips = Trip.objects.all()
    dates = TripDates.objects.all()

    def handle(self, *args, **options):
        """
        Metoda do importowania rezerwacji wycieczek
        Args:
            *args ():
            **options ():

        Returns:

        """
        for i in range(len(self.reservations)):
            ftrip = None
            fdate = None
            for trip in self.trips:
                if str(trip) == self.reservations["trip"][i]:
                    ftrip = trip
            for date in self.dates:
                if str(date) == self.reservations["date"][i]:
                    fdate = date

            _, created = TripReservation.objects.get_or_create(user= get_user_model().objects.get(username=self.reservations["user"][i]),
                                                               trip=ftrip,
                                                               date=fdate,
                                                               persons=int(self.reservations["persons"][i]),
                                                               phone=self.reservations["phone"][i],
                                                               guide=self.reservations["guide"][i],
                                                               room=self.reservations["room"][i],
                                                               all_inclusive=self.reservations["all_inclusive"][i]
                                                               )
            if created:
                logging.info("Dodano rezerwacje dla  ", self.reservations["trip"][i])

