import pandas as pd
import numpy as np
from travels.models import TripReservation
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Creating users accounts"

    reservations = TripReservation.objects.all()
    users = list()
    trips = list()
    recommendations = list()
    full_path = "travels/management/files/algorytm.xlsx"

    def handle(self, *args, **options):
        # pętla pobierająca spisy użytkowników z ich wycieczkami
        for trip in self.reservations:
            self.users.append(trip.user)
            self.trips.append(trip.trip)
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
            for index in df1.index:
                for column in df1.columns:
                    if index == trip.user and column == trip.trip:
                        df1.at[index, column] += 1
        # algorytm
        for wiersz in df1:
            korelacja = df1.corrwith(df1[wiersz])
            tablica = pd.DataFrame(korelacja)
            tablica = tablica.drop([wiersz])
            for wycieczka in range(len(tablica.index)):
                nazwa = tablica.idxmax().item()
                wartosc = tablica[0][nazwa]
                self.recommendations.append([wiersz, nazwa, wartosc])
                tablica = tablica.drop([nazwa])
        # DataFrame rekomendacji
        df2 = pd.DataFrame()
        df2 = df2.append(self.recommendations, ignore_index=True)
        # zapis do excela
        with pd.ExcelWriter(self.full_path) as writer:
            df1.to_excel(writer, sheet_name='Dane')
            df2.to_excel(writer, sheet_name='Rekomendacje')
