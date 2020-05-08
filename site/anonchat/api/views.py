"""Simple API views for use in registering users and generating rooms."""

import json
from uuid import uuid4

from api.models import Room

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

        if not 1 < len(username) < 100:
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
