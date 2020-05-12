"""Models for use in registering rooms and creating messages."""

from django.db import models


class Room(models.Model):
    """Represents a single, ephemeral chatroom."""

    uuid = models.CharField(max_length=32, primary_key=True)
    slug = models.CharField(max_length=50)

    def __str__(self: models.Model) -> str:
        """Represent rooms with their humanhashes."""
        return self.slug


class Message(models.Model):
    """Represents a message in one of our chatrooms."""

    time = models.DateTimeField(auto_now_add=True)
    author = models.CharField(max_length=100)
    content = models.CharField(max_length=256)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
