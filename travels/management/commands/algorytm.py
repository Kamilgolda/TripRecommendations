import pandas as pd
import numpy as np
from travels.models import TripReservation
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Creating users accounts"

    reservations = TripReservation.objects.all()
    users = set()
    trips = set()
    recommendations = list()
    full_path = "travels/management/files/algorytm.xlsx"

    def handle(self, *args, **options):
        # pętla pobierająca spisy użytkowników i wycieczek
        for trip in self.reservations:
            self.users.add(trip.user)
            self.trips.add(trip.trip)
        # lista zerowa
        x = len(self.users)
        y = len(self.trips)
        data = np.zeros((x, y), dtype=int)
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
        # algorytm
        for wiersz in df1:
            # obliczanie podobieństwa wycieczek
            i = 0
            korelacja = df1.corrwith(df1[wiersz])
            tablica = pd.DataFrame(korelacja)
            tablica = tablica.drop([wiersz])
            while i != 10:
                # znalezienie 10 najbardziej podobnych wycieczek
                nazwa = tablica.idxmax().item()
                wartosc = tablica[0][nazwa]
                self.recommendations.append([wiersz, nazwa, wartosc])
                tablica = tablica.drop([nazwa])
                i += 1
        # DataFrame rekomendacji
        df2 = pd.DataFrame()
        df2 = df2.append(self.recommendations, ignore_index=True)
        # zapis do excela
        with pd.ExcelWriter(self.full_path) as writer:
            df1.to_excel(writer, sheet_name='Dane')
            df2.to_excel(writer, sheet_name='Rekomendacje')
