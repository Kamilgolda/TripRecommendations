from django.contrib import admin
from travels.models import Trip, TripPicture, TripDates, TripReservation
#from django.utils.html import format_html

class TripPicturesInline(admin.TabularInline):
    model = TripPicture

class TripDatesInline(admin.TabularInline):
    model = TripDates

class TripsAdmin(admin.ModelAdmin):
    exclude = ("slug",)
    list_display = ("title", "country", "city", "duration", "type", "no_of_terms")
    list_filter = ["country", 'title']
    search_fields = ['title', "country"]
    inlines = [
        TripPicturesInline, TripDatesInline
    ]
    save_as = True

    def no_of_terms(self,obj):
        terms = TripDates.objects.all().filter(trip=obj)
        no = len(terms)
        return no

    no_of_terms.short_description = 'Liczba terminów'


class TripsPicturesAdmin(admin.ModelAdmin):
    list_display = ("trip", "picture", "default")
    list_filter = ['trip']
    search_fields = ['trip']


class TripsDatesAdmin(admin.ModelAdmin):
    list_display = ("trip", "start_date", "end_date")


class TripsReservationAdmin(admin.ModelAdmin):
    exclude = ("price",)
    list_display = ("user", "trip", "persons", "price")


admin.site.register(Trip, TripsAdmin)
admin.site.register(TripPicture, TripsPicturesAdmin)
admin.site.register(TripDates, TripsDatesAdmin)
admin.site.register(TripReservation, TripsReservationAdmin)

