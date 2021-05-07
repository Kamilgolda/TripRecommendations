from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, redirect
from django.shortcuts import render
from .models import TripReservation, Trip, TripPicture, TripDates
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


class TripDetailView(FormMixin,DetailView):
    model = Trip
    context_object_name = "trip"
    form_class = TripReservationForm

    def get_context_data(self, **kwargs):
        context = super(TripDetailView, self).get_context_data(**kwargs)
        context['pictures'] = TripPicture.objects.filter(trip=context['trip'])
        context['dates'] = TripDates.objects.filter(trip=context['trip'])
        context['form'] = self.form_class(initial={'phone': "123"})
        return context

    def get_success_url(self):
        return reverse("travels:details", kwargs={"slug": self.object.slug})

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        print(form['phone'])
        if form.is_valid():
            messages.success(request, f'Rezerwacja została złożona')
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        form.save(False)
        form.user_id = self.request.user.pk
        print(form.cleaned_data)
        form.save()
        return super(TripDetailView, self).form_valid(form)




# class TripReservationCreateView(CreateView):
#     model = TripReservation
#     form_class = TripReservationForm
#
#
# @login_required
# def reservation(request, *args, **kwargs):
#
#     if request.method == 'POST':
#         r_form = TripReservationForm(request.POST)
#         print(r_form['user'])
#         if r_form.is_valid():
#
#             r_form.save(False)
#             data = r_form.cleaned_data
#             data['persons'] = 3
#             print(data)
#             r_form.save()
#
#             messages.success(request, f'Rezerwacja została złożona')
#             path = "/oferty"
#             return redirect(path)
#
#     else:
#         r_form = TripReservationForm()
#
#
#     context = {
#         'form': r_form,
#         'kwargs': kwargs,
#     }
#     return render(request, 'travels/partials/reservation_form.html', context)
