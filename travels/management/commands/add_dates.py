import pandas as pd
import os.path
from django.core.management.base import BaseCommand, CommandError
import logging
from travels.models import Trip, TripDates
import datetime
import random


class Command(BaseCommand):
    """
     Klasa do tworzenia dat wycieczek
    """
    help = "Creating Trips Dates"

    trips = Trip.objects.all()

    def handle(self, *args, **options):
        """
            Tworzenie daty wycieczki
        Args:
            *args ():
            **options ():

        Returns:
            object: TripDates
        """
        for trip in self.trips:
            terms = TripDates.objects.all().filter(trip=trip)
            no = len(terms)
            if no == 0:
                _, created = TripDates.objects.get_or_create(trip=trip,
                                                             start_date=datetime.datetime(2020, 5, random.randint(1, 31))
                                                             )
                if created:
                    logging.info("Dodano 1 Termin dla wycieczki ", trip)

                _, created = TripDates.objects.get_or_create(trip=trip,
                                                             start_date=datetime.datetime(2020, 6,
                                                                                          random.randint(1, 30))
                                                             )
                if created:
                    logging.info("Dodano 2 Termin dla wycieczki ", trip)

                _, created = TripDates.objects.get_or_create(trip=trip,
                                                             start_date=datetime.datetime(2020, 7,
                                                                                          random.randint(1, 31))
                                                             )
                if created:
                    logging.info("Dodano 3 Termin dla wycieczki ", trip)
