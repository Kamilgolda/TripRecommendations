import pandas as pd
import os.path
from django.core.management.base import BaseCommand, CommandError
import logging
from travels.models import Trip, TripDates
import datetime
import random


class Command(BaseCommand):
    """
    Klasa do tworzenia typów wycieczek
    """
    help = "Creating fields in Trips"

    trips = Trip.objects.all().filter(country="Wyspy Zielonego Przylądka")

    def handle(self, *args, **options):
        """
        Metoda do tworzenia typów wycieczek
        Args:
            *args ():
            **options ():
        """
        for trip in self.trips:
            trip.countryEN = "United Arab Emirates"
            trip.currency = "CVE"
            trip.climate = "Morski"
            trip.rating = random.uniform(1, 6)
            trip.save()
