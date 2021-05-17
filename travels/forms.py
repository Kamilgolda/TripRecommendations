from django.forms import ModelForm, HiddenInput
from travels.models import TripReservation, Polling
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, ButtonHolder, Submit, Row, Column
from django.utils.translation import gettext as _
from django import forms


class TripReservationForm(ModelForm):

    select_dates = []

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_tag = True
        self.fields['user'].widget = HiddenInput()
        self.fields['trip'].widget = HiddenInput()
        self.fields['date'].widget = forms.Select(choices=self.select_dates)

        self.helper.layout = Layout(Fieldset(
            _("Złóż rezerwację"),
            "date",
            "persons",
            "phone",
            "guide",
            "room",
            "all_inclusive",
            "trip",
            "user",
            ),
            ButtonHolder(Submit("submit", "Rezerwuj", css_class="button white")),
        )

    class Meta:
        model = TripReservation
        fields = '__all__'


class PollingForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_tag = True
        self.fields['user'].widget = HiddenInput()

        self.helper.layout = Layout(Fieldset(
            _("Ankieta"),
            Row(
                Column("preferred_place", css_class="form-group col-md-8 mb-0")
            ),
            Row(
                Column("preferred_transport", css_class="form-group col-md-8 mb-0")
            ),
            Row(
                Column("preferred_type", css_class="form-group col-md-8 mb-0")
            ),
            Row(
                Column("preferred_landscape", css_class="form-group col-md-8 mb-0")
            ),
            "user",
            ),
            ButtonHolder(Submit("submit", "Wyślij", css_class="button white")),
        )

    class Meta:
        model = Polling
        fields = '__all__'
