"""URL configuration for the chat app."""

from chat.views import ChatRoomView, LogoutUserView

from django.urls import path
from django.views.generic import TemplateView


urlpatterns = [
    path('', TemplateView.as_view(template_name='index.html')),
    path('logout', LogoutUserView.as_view()),
    path('<slug:slug>', ChatRoomView.as_view())
]
