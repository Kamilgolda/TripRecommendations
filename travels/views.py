from django.contrib import messages
from .models import Trip, TripPicture, TripDates, Polling, TripReservation
from django.views.generic.edit import CreateView
from .forms import TripReservationForm, PollingForm
from django.views.generic.list import ListView
from django.views.generic import DetailView
from django.views.generic.edit import FormMixin
from django.urls import reverse_lazy
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin
import travels.content_based_recommendation as cbr
from travels.test import Test
import travels.memory_based_collaborative_filtering as mbcf


class SelectedForYouListView(ListView):
    model = Trip
    template_name = 'travels/trip_list.html'
    paginate_by = 12
    context_object_name = "trips"
    ankieta = None

    def get_context_data(self, **kwargs):
        context = super(SelectedForYouListView, self).get_context_data(**kwargs)
        context['pictures'] = TripPicture.objects.all().filter(default=True, trip__in=self.get_queryset()[:50])
        if self.request.user.is_authenticated:
            context['polling'] = self.ankieta
        return context

    def get_queryset(self):
        if self.request.user.is_authenticated:
            user_reservations = TripReservation.manager_objects.user_reservations(self.request.user)
            result_set = set()
            for reservation in user_reservations:
                try:
                    result_set.update(cbr.get_result(reservation.trip.title))
                except IndexError:
                    print("Brak wycieczki w V2csv.csv")
                except Exception:
                    print("Error")
            self.ankieta = Polling.objects.filter(user=self.request.user).last()
            if self.ankieta is not None:
                polling_query = Test.get_polling_query(self.ankieta)
                for trip in polling_query:
                    if not result_set.__contains__(trip.title):
                        result_set.add(trip.title)
            query = Trip.objects.filter(title__in=result_set).order_by('-rating')
            return query

        return Trip.objects.none()


class PopularListView(ListView):
    model = Trip
    paginate_by = 12
    context_object_name = "trips"
    template_name = "travels/trip_list.html"

    def get_context_data(self, **kwargs):
        context = super(PopularListView, self).get_context_data(**kwargs)
        context['pictures'] = TripPicture.objects.all().filter(default=True, trip__in=self.get_queryset()[:50])
        if self.request.user.is_authenticated:
            context['polling'] = Polling.objects.filter(user=self.request.user).last()
        return context

    def get_queryset(self):
        return Test.popular


class OthersChooseListView(ListView):
    model = Trip
    paginate_by = 12
    context_object_name = "trips"

    def get_context_data(self, **kwargs):
        context = super(OthersChooseListView, self).get_context_data(**kwargs)
        context['pictures'] = TripPicture.objects.all().filter(default=True, trip__in=self.get_queryset()[:50])
        if self.request.user.is_authenticated:
            context['polling'] = Polling.objects.filter(user=self.request.user).last()
        return context

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return mbcf.get_result(self.request.user)
        return Trip.objects.none()


class TripDetailView(FormMixin, DetailView):
    model = Trip
    context_object_name = "trip"
    form_class = TripReservationForm

    def get_context_data(self, **kwargs):
        context = super(TripDetailView, self).get_context_data(**kwargs)
        context['pictures'] = TripPicture.objects.all().filter(trip=context['trip'])
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


