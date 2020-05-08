"""Register database models in the admin site."""

from api.models import Message, Room

from django.contrib import admin


admin.site.register(Room)
admin.site.register(Message)
