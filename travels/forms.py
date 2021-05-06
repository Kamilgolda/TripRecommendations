from django.forms import ModelForm
from travels.models import TripReservation


class TripReservationForms(ModelForm):

    class Meta:
        model = TripReservation
        fields = ['user', 'trip', 'persons', 'phone', 'guide', 'room', 'price']
