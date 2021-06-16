import os

from travels.models import TripReservation, Trip
import pandas as pd


def get_result(user):
    user_reservations = TripReservation.manager_objects.user_reservations(user)
    trips = set()
    for reservation in user_reservations:
        trips.add(reservation.trip.__str__())
    recommended_travels_ids = set()
    full_path = 'travels/management/files/mbcf.xlsx'
    exists = os.path.isfile(full_path)
    if exists:
        travels = pd.read_excel(full_path, sheet_name="Rekomendacje")
        recommended_travels = set()
        for trip in trips:
            for i in range(len(travels)):
                if travels[0][i] == trip:
                    recommended_travels.add(travels[1][i])
        recommended_travels.difference_update(trips)
        all_trips = Trip.objects.all()
        for trip in all_trips:
            if recommended_travels.__contains__(str(trip)):
                recommended_travels_ids.add(trip.pk)

        query = Trip.objects.filter(pk__in=recommended_travels_ids).order_by('-rating')
        return query
    else:
        return Trip.objects.none()
