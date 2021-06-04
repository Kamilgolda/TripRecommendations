from sklearn.cluster import KMeans
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from django.core.management.base import BaseCommand


class Command(BaseCommand):

    full_path = "travels/management/files/V1csv.csv"

    df = pd.read_csv(full_path, delimiter=';')

    def handle(self, *args, **options):

        scaler = MinMaxScaler()

        scaler.fit(self.df[['price']])
        self.df['price'] = scaler.transform(self.df[['price']])

        scaler.fit(self.df[['hotelstars']])
        self.df['hotelstars'] = scaler.transform(self.df[['hotelstars']])

        scaler.fit(self.df[['timezone']])
        self.df['timezone'] = scaler.transform(self.df[['timezone']])

        scaler.fit(self.df[['duration']])
        self.df['duration'] = scaler.transform(self.df[['duration']])

        scaler.fit(self.df[['countryId']])
        self.df['countryId'] = scaler.transform(self.df[['countryId']])

        scaler.fit(self.df[['temperatura']])
        self.df['temperatura'] = scaler.transform(self.df[['temperatura']])

        scaler.fit(self.df[['landscape']])
        self.df['landscape'] = scaler.transform(self.df[['landscape']])

        scaler.fit(self.df[['type']])
        self.df['type'] = scaler.transform(self.df[['type']])

        scaler.fit(self.df[['transport']])
        self.df['transport'] = scaler.transform(self.df[['transport']])

        km = KMeans(n_clusters=20)

        y_predicted = km.fit_predict(self.df[['hotelstars', 'timezone', 'price', 'duration', 'countryId', 'temperatura',
                                         'landscape', 'type', 'transport']])
        self.df['cluster'] = y_predicted
        self.df.to_csv(r'travels/management/files/V2csv.csv', index=False)
