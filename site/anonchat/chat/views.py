"""Template views for rendering chatrooms and registering users."""

from api.models import Room

from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.views.generic.base import TemplateView, View


class LogoutUserView(View):
    """GET requests to this view delete session data."""

    def get(self: View, request: HttpRequest) -> HttpResponse:
        """Logout a user, and delete their associated chatroom."""
        ...


class ChatRoomView(TemplateView):
    """Render a room if it exists, otherwise return a 404 page."""

    def get(self: View, request: HttpRequest, slug: str) -> HttpResponse:
        """Find a room that matches the provided slug."""
        room = Room.objects.filter(slug=slug).first()
        if room is not None:
            return render(
                request,
                'room.html',
                context=dict(room=room)
            )
        else:
            return render(
                request,
                '404.html',
                status=404,
                context=dict(room=slug)
            )
