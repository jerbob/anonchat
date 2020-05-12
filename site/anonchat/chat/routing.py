"""URL configuration for Websocket consumers in the chat app."""

from chat import consumers

from django.urls import re_path


websocket_urlpatterns = [
    re_path(r'ws/rooms/(?P<slug>[a-z\-]+)$', consumers.ChatConsumer),
]
