from django.core.management.base import BaseCommand
import numpy as np
import pandas as pd


class Command(BaseCommand):

    full_path = "travels/management/files/V2csv.csv"

    df = pd.read_csv(full_path, delimiter=',')

    def handle(self, trip_name, *args, **options):
        trip_id = self.df[self.df.title == trip_name]["id"].values[0]
        # trip_cluster = self.df[self.df.title == trip_name]["cluster"].values[0]

        X = self.df
        X2 = self.df
        X = X.drop(['title', 'climate', 'country', 'id', 'cluster'], axis=1)

        y = self.df[self.df.title == trip_name]
        y = y.drop(['title', 'climate', 'country', 'id', 'cluster'], axis=1)

        X = X.values
        y = y.values
        distances = np.linalg.norm(X - y, axis=1)
        X2['distance'] = distances
        X3 = X2.sort_values(by=['distance'])
        print(X3)


command = Command()
command.handle('Hotel Odysee Resort')
