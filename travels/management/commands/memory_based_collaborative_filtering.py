import os

import pandas as pd
import numpy as np
from travels.models import TripReservation
from django.core.management.base import BaseCommand
from time import strftime

class Command(BaseCommand):
    help = "Memory Based Collaborative filtering"

    reservations = TripReservation.objects.all()
    users = set()
    trips = set()
    recommendations = list()
    full_path = "travels/management/files/mbcf.xlsx"

    def handle(self, *args, **options):
        # uruchomienie o polnocy
        if strftime("%H:%M:%S") == "00:00:00":
            print("generating mbcf - Memory Based Collaborative filtering\n Please wait...")
            # pętla pobierająca spisy użytkowników i wycieczek
            for trip in self.reservations:
                self.users.add(trip.user)
                self.trips.add(trip.trip)
            # lista zerowa
            x = len(self.users)
            y = len(self.trips)
            data = np.zeros((x, y), dtype=int)

            print("10%...")
            # DataFrame zerowy
            df1 = pd.DataFrame(data)
            df1.index = self.users
            df1.columns = self.trips
            # pętla zapisująca rezerwacje do DataFrame'u
            for trip in self.reservations:
                for i, index in enumerate(df1.index):
                    if index == trip.user:
                        for j, column in enumerate(df1.columns):
                            if column == trip.trip:
                                df1.iat[i, j] += 1
            print("40%...")
            # algorytm
            for wiersz in df1:
                # obliczanie podobieństwa wycieczek
                i = 0
                korelacja = df1.corrwith(df1[wiersz])
                tablica = pd.DataFrame(korelacja)
                tablica = tablica.drop([wiersz])
                while i != 4:
                    # znalezienie 10 najbardziej podobnych wycieczek
                    nazwa = tablica.idxmax().item()
                    wartosc = tablica[0][nazwa]
                    self.recommendations.append([wiersz, nazwa, wartosc])
                    tablica = tablica.drop([nazwa])
                    i += 1
            print("90%...")
            # DataFrame rekomendacji
            df2 = pd.DataFrame()
            df2 = df2.append(self.recommendations, ignore_index=True)
            # zapis do excela
            if os.path.exists(self.full_path):
                os.remove(self.full_path)
            with pd.ExcelWriter(self.full_path) as writer:
                df1.to_excel(writer, sheet_name='Dane')
                df2.to_excel(writer, sheet_name='Rekomendacje')
            print("100%")
            print("generating mbcf - Memory Based Collaborative filtering DONE")
