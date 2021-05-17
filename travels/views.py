from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Trip, TripPicture, TripDates, Polling
from django.views.generic.edit import CreateView
from .forms import TripReservationForm, PollingForm
from django.views.generic.list import ListView
from django.views.generic import DetailView, FormView
from django.views.generic.edit import FormMixin
from django.urls import reverse_lazy
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User


class SelectedForYouListView(ListView):
    model = Trip
    paginate_by = 10
    context_object_name = "trips"

    def get_context_data(self, **kwargs):
        context = super(SelectedForYouListView, self).get_context_data(**kwargs)
        context['pictures'] = TripPicture.objects.all().filter(default=True)
        if self.request.user.is_authenticated:
            context['polling'] = Polling.objects.filter(user=self.request.user)[:1]
        return context

    def get_queryset(self):
        if self.request.user.is_authenticated:
            ankieta = Polling.objects.filter(user=self.request.user)[:1]
            if len(ankieta) > 0:
                ankieta = ankieta[0]
                if ankieta.preferred_place == 'Tylko po Polsce':
                    query = Trip.objects.filter(country="Polska",
                                                type=ankieta.preferred_type,
                                                transport=ankieta.preferred_transport,
                                                landscape=ankieta.preferred_landscape
                                                )
                    if len(query) < 5:
                        query = Trip.objects.filter(country="Polska",
                                                    type=ankieta.preferred_type,
                                                    transport=ankieta.preferred_transport
                                                    )
                    if len(query) < 5:
                        query = Trip.objects.filter(country="Polska",
                                                    type=ankieta.preferred_type
                                                    )
                    if len(query) < 5:
                        query = Trip.objects.filter(country="Polska"
                                                    )

                if ankieta.preferred_place == 'Tylko za granicą':
                    query = Trip.objects.filter(type=ankieta.preferred_type,
                                                transport=ankieta.preferred_transport,
                                                landscape=ankieta.preferred_landscape
                                                ).exclude(country="Polska")
                    if len(query) < 5:
                        query = Trip.objects.filter(type=ankieta.preferred_type,
                                                    transport=ankieta.preferred_transport
                                                    ).exclude(country="Polska")
                    if len(query) < 5:
                        query = Trip.objects.filter(type=ankieta.preferred_type
                                                    ).exclude(country="Polska")
                    if len(query) < 5:
                        query = Trip.objects.exclude(country="Polska")

                if ankieta.preferred_place == 'Po Polsce oraz za granicą':
                    query = Trip.objects.filter(type=ankieta.preferred_type,
                                                transport=ankieta.preferred_transport,
                                                landscape=ankieta.preferred_landscape)
                    if len(query) < 5:
                        query = Trip.objects.filter(type=ankieta.preferred_type,
                                                    transport=ankieta.preferred_transport
                                                    )
                    if len(query) < 5:
                        query = Trip.objects.filter(type=ankieta.preferred_type)
                return query

        return Trip.objects.none()


class PopularListView(ListView):
    model = Trip
    paginate_by = 10
    context_object_name = "trips"

    def get_context_data(self, **kwargs):
        context = super(PopularListView, self).get_context_data(**kwargs)
        context['pictures'] = TripPicture.objects.all().filter(default=True)
        if self.request.user.is_authenticated:
            context['polling'] = Polling.objects.filter(user=self.request.user)[:1]
        return context

    def get_queryset(self):
        return Trip.objects.all()


class OthersChooseListView(ListView):
    model = Trip
    paginate_by = 10
    context_object_name = "trips"

    def get_context_data(self, **kwargs):
        context = super(OthersChooseListView, self).get_context_data(**kwargs)
        context['pictures'] = TripPicture.objects.all().filter(default=True)
        if self.request.user.is_authenticated:
            context['polling'] = Polling.objects.filter(user=self.request.user)[:1]
        return context

    def get_queryset(self):
        return Trip.objects.all()



class TripDetailView(FormMixin, DetailView):
    model = Trip
    context_object_name = "trip"
    form_class = TripReservationForm

    def get_context_data(self, **kwargs):
        context = super(TripDetailView, self).get_context_data(**kwargs)
        context['pictures'] = TripPicture.objects.filter(trip=context['trip'])
        context['dates'] = TripDates.objects.filter(trip=context['trip'])
        TripReservationForm.select_dates=self.get_data(context['dates'])
        context['form'] = self.form_class(initial={'user': self.request.user, 'trip': self.object})

        return context

    def get_success_url(self):
        return reverse("travels:details", kwargs={"slug": self.object.slug})

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            messages.success(request, f'Rezerwacja została złożona')
            return self.form_valid(form)
        else:
            print(form.cleaned_data)
            return self.form_invalid(form)

    def form_valid(self, form):
        form.save(False)
        print(form.cleaned_data)
        form.save()
        return super(TripDetailView, self).form_valid(form)

    def get_data(self, data):
        choices = list(data)
        select_dates = []
        for value in choices:
            select_dates.append((value.pk, value.start_date))
        return select_dates


class QuestionnaireView(LoginRequiredMixin, CreateView):
    model = Polling
    form_class = PollingForm
    success_url = reverse_lazy('travels:selected_for_you')

    def get_initial(self):
        return {'user': self.request.user}

    def form_valid(self, form):
        result = super().form_valid(form)
        messages.success(self.request, f'Dziękujemy za wypełnienie ankiety')
        return result
