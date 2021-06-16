from django.urls import path
from . import views

from travels.views import (SelectedForYouListView, TripDetailView, QuestionnaireView, PopularListView, OthersChooseListView)

app_name = "travels"
urlpatterns = [
    path("", PopularListView.as_view(), name="popular"),
    path("selectedforyou", SelectedForYouListView.as_view(), name="selected_for_you"),
    path("otherschoose", OthersChooseListView.as_view(), name="otherschoose"),
    path("polling", QuestionnaireView.as_view(), name="polling"),
    path("<str:slug>/", TripDetailView.as_view(), name="details"),
]
