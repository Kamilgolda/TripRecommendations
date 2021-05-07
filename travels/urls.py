from django.urls import path
from . import views

from travels.views import (TripsListView, TripDetailView)

app_name = "travels"
urlpatterns = [
    path("", TripsListView.as_view(), name="list"),
    path("<str:slug>/", TripDetailView.as_view(), name="details"),
]
