from django.contrib import admin
from travels.models import Trip, TripPicture, TripDates
#from django.utils.html import format_html


class TripsAdmin(admin.ModelAdmin):
    exclude = ("slug",)
    list_display = ("title", "country", "type")


class TripsPicturesAdmin(admin.ModelAdmin):
    list_display = ("trip", "picture")


class TripsDatesAdmin(admin.ModelAdmin):
    list_display = ("trip", "start_date", "end_date")


admin.site.register(Trip, TripsAdmin)
admin.site.register(TripPicture, TripsPicturesAdmin)
admin.site.register(TripDates, TripsDatesAdmin)

