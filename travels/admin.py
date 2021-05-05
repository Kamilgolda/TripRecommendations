from django.contrib import admin
from travels.models import Trip, TripPicture, TripDates, TripReservation
#from django.utils.html import format_html


class TripsAdmin(admin.ModelAdmin):
    exclude = ("slug",)
    list_display = ("title", "country", "type")


class TripsPicturesAdmin(admin.ModelAdmin):
    list_display = ("trip", "picture")


class TripsDatesAdmin(admin.ModelAdmin):
    list_display = ("trip", "start_date", "end_date")


class TripsReservationAdmin(admin.ModelAdmin):
    exclude = ("price",)
    list_display = ("user", "trip", "persons", "price")


admin.site.register(Trip, TripsAdmin)
admin.site.register(TripPicture, TripsPicturesAdmin)
admin.site.register(TripDates, TripsDatesAdmin)
admin.site.register(TripReservation, TripsReservationAdmin)

