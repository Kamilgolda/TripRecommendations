import pandas as pd
import os.path
from django.core.management.base import BaseCommand, CommandError
import logging
from travels.models import Trip

# full_path = os.path.join("../files/Wycieczki.xlsx")
# trips = pd.read_excel(full_path, sheet_name='Góry')
# print(trips["Nazwa wycieczki"])


class Command(BaseCommand):
    help = "Creating trips"

    full_path = 'travels/management/files/Wycieczki.xlsx'
    trips = pd.read_excel(full_path, sheet_name='Zwiedzanie')

    def handle(self, *args, **options):
        for i in range(len(self.trips)):
            _, created = Trip.objects.get_or_create(title=self.trips["Nazwa wycieczki"][i],
                                                    # hotelstars=self.trips["Gwiazdki hotelu"][i],
                                                    country=self.trips["Kraj"][i],
                                                    timezone=self.trips["Strefa czasowa"][i],
                                                    landscape=self.trips["Krajobraz"][i],
                                                    type=self.trips["Rodzaj wycieczki"][i],
                                                    transport=self.trips["Rodzaj podróży"][i],
                                                    price=self.trips["Cena"][i],
                                                    duration=self.trips["Ilość dni"][i],
                                                    )
            if created:
                logging.info("Dodano Wycieczkę ", self.trips["Nazwa wycieczki"][i])
