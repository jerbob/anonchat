"""URL configuration for the api app."""

from api.views import PostMessageView, RegisterUserView

from django.urls import path


urlpatterns = [
    path('register', RegisterUserView.as_view()),
    path('rooms/<slug:slug>/post', PostMessageView.as_view())
]
