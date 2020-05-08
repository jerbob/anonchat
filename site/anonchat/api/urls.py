"""URL configuration for the api app."""

from api.views import RegisterUserView

from django.urls import path


urlpatterns = [
    path('register', RegisterUserView.as_view())
]
