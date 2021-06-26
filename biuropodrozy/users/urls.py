from django.urls import path

from biuropodrozy.users.views import (
    user_detail_view,
    user_redirect_view,
    user_update_view,
    user_delete_view,
    del_user,
    user_reservations_view
)

app_name = "users"
urlpatterns = [
    path("~redirect/", view=user_redirect_view, name="redirect"),
    path("~update/", view=user_update_view, name="update"),
    path("reservations/", view=user_reservations_view, name="reservations"),
    path("delete/", view=user_delete_view, name="delete"),
    path("delconfirm/", view=del_user, name="deleteconfirm"),
    path("<str:username>/", view=user_detail_view, name="detail"),


]
