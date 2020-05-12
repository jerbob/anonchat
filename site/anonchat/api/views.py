"""Simple API views for use in registering users and generating rooms."""

import json
from uuid import uuid4

from api.models import Message, Room

from django.http import HttpRequest, JsonResponse
from django.views.generic import View

from humanhash import humanize


class RegisterUserView(View):
    """POST to this endpoint to register a user."""

    def post(self: View, request: HttpRequest) -> JsonResponse:
        """Create a user, provided the username."""
        payload = json.loads(request.body.decode())
        username = str(payload.get('username', ''))

        if request.session.get('registered'):
            return JsonResponse({
                'success': False,
                'error': 'You are already registered.'
            })

        if not 1 <= len(username) <= 100:
            return JsonResponse({
                'success': False,
                'error': 'Username must be between 1 and 100.'
            })

        digest = uuid4().hex
        slug = humanize(digest)

        request.session['slug'] = slug
        request.session['registered'] = True
        request.session['username'] = username

        room = Room(uuid=digest, slug=slug)
        room.save()
        return JsonResponse({
            'success': True,
            'slug': slug
        })


class PostMessageView(View):
    """POST to this endpoint to send a message."""

    def post(self: View, request: HttpRequest, slug: str) -> JsonResponse:
        """Add a new message to the specified room."""
        payload = json.loads(request.body.decode())
        content = str(payload.get('content', ''))

        if not 1 <= len(content) <= 256:
            return JsonResponse({
                'success': False,
                'error': 'Content must be between 1 and 256.'
            })

        if not request.session.get('registered'):
            return JsonResponse({
                'success': False,
                'error': 'You are not registered.'
            })

        room = Room.objects.filter(slug=slug).first()
        if room is None:
            return JsonResponse({
                'success': False,
                'error': 'That room does not exist.'
            })

        message = Message(
            author=request.session.get('username'),
            content=content,
            room=room
        )
        message.save()

        return JsonResponse({
            'success': True,
            'message': {
                'content': message.content,
                'author': message.author
            }
        })
