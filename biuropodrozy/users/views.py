from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.views.generic import DetailView, RedirectView, UpdateView
from django.views.generic import TemplateView
from django.shortcuts import render
from django.contrib import messages


User = get_user_model()


class UserDetailView(LoginRequiredMixin, DetailView):

    model = User
    slug_field = "username"
    slug_url_kwarg = "username"


user_detail_view = UserDetailView.as_view()


class UserUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):

    model = User
    fields = ["name"]
    success_message = _("Information successfully updated")

    def get_success_url(self):
        return self.request.user.get_absolute_url()  # type: ignore [union-attr]

    def get_object(self):
        return self.request.user


user_update_view = UserUpdateView.as_view()


class UserDeleteView(TemplateView):
    template_name = 'users/user_delete.html'


user_delete_view = UserDeleteView.as_view()


def del_user(request):
    try:
        u = request.user
        u.delete()
        messages.success(request, 'Konto zostało usunięte')

    except User.DoesNotExist:
        messages.error(request, 'Użytkownik nie istnieje')
        return render(request, 'pages/home.html')

    except Exception:
        messages.error(request, 'Wystąpił błąd')
        return render(request, 'pages/home.html')

    return render(request, 'pages/home.html')


class UserRedirectView(LoginRequiredMixin, RedirectView):

    permanent = False

    def get_redirect_url(self):
        return reverse("users:detail", kwargs={"username": self.request.user.username})


user_redirect_view = UserRedirectView.as_view()
