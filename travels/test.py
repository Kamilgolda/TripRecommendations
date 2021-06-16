from travels.models import Trip, TripReservation
import pandas as pd
from django.core.management import call_command


class Test:
    popular = Trip.manager_objects.popular_trips()
    content_based_recommendation_df = pd.read_csv("travels/management/files/V2csv.csv", delimiter=',')
    generating_xlsx_mbcf = call_command("memory_based_collaborative_filtering")
    @staticmethod
    def get_polling_query(ankieta):
        if ankieta.preferred_place == 'Tylko po Polsce':
            query = Trip.objects.filter(country="Polska",
                                        type=ankieta.preferred_type,
                                        transport=ankieta.preferred_transport,
                                        landscape=ankieta.preferred_landscape
                                        )
            if len(query) < 5:
                query = Trip.objects.filter(country="Polska",
                                            type=ankieta.preferred_type,
                                            transport=ankieta.preferred_transport
                                            )

        if ankieta.preferred_place == 'Tylko za granicą':
            query = Trip.objects.filter(type=ankieta.preferred_type,
                                        transport=ankieta.preferred_transport,
                                        landscape=ankieta.preferred_landscape
                                        ).exclude(country="Polska")
            if len(query) < 5:
                query = Trip.objects.filter(type=ankieta.preferred_type,
                                            transport=ankieta.preferred_transport
                                            ).exclude(country="Polska")

        if ankieta.preferred_place == 'Po Polsce oraz za granicą':
            query = Trip.objects.filter(type=ankieta.preferred_type,
                                        transport=ankieta.preferred_transport,
                                        landscape=ankieta.preferred_landscape)
            if len(query) < 5:
                query = Trip.objects.filter(type=ankieta.preferred_type,
                                            transport=ankieta.preferred_transport
                                            )

        return query
