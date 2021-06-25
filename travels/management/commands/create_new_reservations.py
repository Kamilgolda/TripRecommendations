import pandas as pd
import os.path
from django.core.management.base import BaseCommand, CommandError
import logging
from travels.models import Trip, TripDates, TripReservation
from django.contrib.auth import get_user_model
import datetime
import random


class Command(BaseCommand):
    """
    Klasa do tworzenia nowych rezerwacji
    """
    help = "Creating Reservations"

    dates = TripDates.objects.all()
    my_users = get_user_model().objects.all()

    print(dates[0])


    def handle(self, *args, **options):
        """
        Tworzy rezerwacje wycieczek z losowymi polami dla losowych wycieczek
        Args:
            *args ():
            **options ():
        """
        for idx, user in enumerate(self.my_users):
            quantity = random.randint(1, 5)
            list_random_dates = []
            for i in range(0, quantity):
               date = self.dates[random.randint(0, len(self.dates)-1)]
               if len(list_random_dates) == 0:
                  list_random_dates.append(date)
               else:
                   for dt in list_random_dates:
                       while dt.trip.title == date.trip.title:
                           date = self.dates[random.randint(0, len(self.dates) - 1)]
                   list_random_dates.append(date)
            print(list_random_dates)
            print("**************************")


            for dt in list_random_dates:

                _, created = TripReservation.objects.get_or_create(user=user,
                                                                   trip=dt.trip,
                                                                   date =dt,
                                                                   persons= random.randint(1, 5),
                                                                   phone = random.randint(100000000, 999999999),
                                                                   guide= random.choice([True, False]),
                                                                   room= random.choice([True, False]),
                                                                   all_inclusive= random.choice([True, False])
                                                                 )
                if created:
                     logging.info("Dodano rezerwację dla", user)

