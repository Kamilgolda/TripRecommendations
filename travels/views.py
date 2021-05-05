from django.shortcuts import render
from .models import TripReservation
from django.views.generic.edit import CreateView
from .forms import TripReservationForms
# Create your views here.


class TripReservationCreateView(CreateView):
    model = TripReservation
    form_class = TripReservationForms
