"""URL configuration for the chat app."""

from chat.views import ChatRoomView

from django.urls import path
from django.views.generic import TemplateView


urlpatterns = [
    path('', TemplateView.as_view(template_name='index.html')),
    path('<slug:slug>', ChatRoomView.as_view())
]
