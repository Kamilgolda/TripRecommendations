from django.shortcuts import render
from .models import TripReservation, Trip, TripPicture
from django.views.generic.edit import CreateView
from .forms import TripReservationForms
from django.views.generic.list import ListView
from django.views.generic import DetailView
# Create your views here.


class TripsListView(ListView):
    model = Trip
    paginate_by = 10
    context_object_name = "trips"

    def get_context_data(self, **kwargs):
        context = super(TripsListView, self).get_context_data(**kwargs)
        context['pictures'] = TripPicture.objects.all().filter(default=True)
        return context


class TripDetailView(DetailView):
    model = Trip
    context_object_name = "trip"

    def get_context_data(self, **kwargs):
        context = super(TripDetailView, self).get_context_data(**kwargs)
        context['pictures'] = TripPicture.objects.all()
        return context


class TripReservationCreateView(CreateView):
    model = TripReservation
    form_class = TripReservationForms
