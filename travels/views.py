from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Trip, TripPicture, TripDates
from django.views.generic.edit import CreateView
from .forms import TripReservationForm
from django.views.generic.list import ListView
from django.views.generic import DetailView
from django.views.generic.edit import FormMixin
from django.urls import reverse_lazy
from django.urls import reverse

# Create your views here.


class TripsListView(ListView):
    model = Trip
    paginate_by = 10
    context_object_name = "trips"

    def get_context_data(self, **kwargs):
        context = super(TripsListView, self).get_context_data(**kwargs)
        context['pictures'] = TripPicture.objects.all().filter(default=True)
        return context


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
