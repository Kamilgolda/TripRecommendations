import numpy as np
import pandas as pd
from travels.helper import Helper


def get_result(trip_name):
    # full_path = "travels/management/files/V2csv.csv"
    df = Helper.content_based_recommendation_df
    print(trip_name)
    trip_id = df[df.title == trip_name]["id"].values[0]
    # trip_cluster = self.df[self.df.title == trip_name]["cluster"].values[0]

    X = df
    X2 = df
    X = X.drop(['title', 'climate', 'country', 'id', 'cluster'], axis=1)

    y = df[df.title == trip_name].head(1)
    y = y.drop(['title', 'climate', 'country', 'id', 'cluster'], axis=1)

    X = X.values
    y = y.values
    distances = np.linalg.norm(X - y, axis=1)
    X2['distance'] = distances
    X3 = X2.sort_values(by=['distance'])
    result = set()
    for x in X3['title'][1:11]:
        result.add(x)
    print(result)
    return result
