from django.urls import path
from . import views

from travels.views import (SelectedForYouListView, TripDetailView, QuestionnaireView, PopularListView, OthersChooseListView)

app_name = "travels"
urlpatterns = [
    path("", SelectedForYouListView.as_view(), name="selected_for_you"),
    path("popular", PopularListView.as_view(), name="popular"),
    path("otherschoose", PopularListView.as_view(), name="otherschoose"),
    path("polling", QuestionnaireView.as_view(), name="polling"),
    path("<str:slug>/", TripDetailView.as_view(), name="details"),
]
