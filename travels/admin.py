from django.contrib import admin
from travels.models import Trip, TripPicture, TripDates, TripReservation, Polling
#from django.utils.html import format_html


class TripPicturesInline(admin.TabularInline):
    """
    Klasa odpowiedziala za filtrowanie klasy TripPicture w palelu admina
    """
    model = TripPicture


class TripDatesInline(admin.TabularInline):
    """
     Klasa odpowiedziala za filtrowanie klasy TripDates w palelu admina
    """
    model = TripDates


class TripsAdmin(admin.ModelAdmin):
    """
         Klasa odpowiedziala za filtrowanie klasy Trip w palelu admina
    """
    exclude = ("slug",)
    list_display = ("title", "country", "city", "duration", "type", "no_of_terms")
    list_filter = ["country", 'title']
    search_fields = ['title', "country"]
    inlines = [
        TripPicturesInline, TripDatesInline
    ]
    save_as = True

    def no_of_terms(self, obj):
        """
        Metoda zwraca długoćś terminów wycieczek
        """
        terms = TripDates.objects.all().filter(trip=obj)
        no = len(terms)
        return no

    no_of_terms.short_description = 'Liczba terminów'


class TripsPicturesAdmin(admin.ModelAdmin):
    """
    Klasa odpowiedziala za filtrowanie klasy TripsPictures w palelu admina
    """
    list_display = ("trip", "picture", "default")
    list_filter = ['trip']
    search_fields = ['trip']


class TripsDatesAdmin(admin.ModelAdmin):
    """
    Klasa odpowiedziala za filtrowanie klasy TripsDates w palelu admina
    """
    list_display = ("trip", "start_date", "end_date")


class TripsReservationAdmin(admin.ModelAdmin):
    """
     Klasa odpowiedziala za filtrowanie klasy TripsReservation w palelu admina
    """
    list_display = ("user", "trip", "persons", "price")
    list_filter = ['trip', 'user']
    search_fields = ['user']


class PollingAdmin(admin.ModelAdmin):
    """
        Klasa odpowiedziala za filtrowanie klasy Polling w palelu admina
       """
    list_display = ["user"]
    list_filter = ['user']


# rejestracja modeli w panelu admina
admin.site.register(Trip, TripsAdmin)
admin.site.register(TripPicture, TripsPicturesAdmin)
admin.site.register(TripDates, TripsDatesAdmin)
admin.site.register(TripReservation, TripsReservationAdmin)
admin.site.register(Polling, PollingAdmin)

