"""Routing configuration for Websocket consumers."""

from channels.routing import ProtocolTypeRouter, URLRouter
from channels.sessions import SessionMiddlewareStack

import chat.routing


application = ProtocolTypeRouter({
    'websocket': SessionMiddlewareStack(
        URLRouter(chat.routing.websocket_urlpatterns)
    ),
})
