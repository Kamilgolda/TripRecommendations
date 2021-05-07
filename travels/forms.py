from django.forms import ModelForm
from travels.models import TripReservation
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, ButtonHolder, Submit, Row, Column
from django.utils.translation import gettext as _


class TripReservationForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_tag = True

        self.helper.layout = Layout(Fieldset(
            _("Create new fact entry"),
            Row(
                Column("persons", css_class="form-group col-md-8 mb-0")
            ),
            "phone",
            "guide",
            "room",
            "trip",

            ),
            ButtonHolder(Submit("submit", "Submit", css_class="button white")),
        )

    class Meta:
        model = TripReservation
        #fields = '__all__'
        exclude = ("user", "price",)
