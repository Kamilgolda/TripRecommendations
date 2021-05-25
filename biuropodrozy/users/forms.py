from django.contrib.auth import forms as admin_forms
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, ButtonHolder, Submit, Row, Column
from django.forms import ModelForm
from biuropodrozy.users.models import Contact

User = get_user_model()


class UserChangeForm(admin_forms.UserChangeForm):
    class Meta(admin_forms.UserChangeForm.Meta):
        model = User


class UserCreationForm(admin_forms.UserCreationForm):
    class Meta(admin_forms.UserCreationForm.Meta):
        model = User

        error_messages = {
            "username": {"unique": _("This username has already been taken.")}
        }


class ContactForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_tag = True

        self.helper.layout = Layout(Fieldset(
            _(""),
            Row(
                Column("email", css_class="form-group col-md-8 mb-0")
            ),
            "description",
            ),
            ButtonHolder(Submit("submit", "Wyślij", css_class="button white")),
        )

    class Meta:
        model = Contact
        fields = "__all__"
