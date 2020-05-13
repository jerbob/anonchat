"""Test constraints for Room and Message models."""

from datetime import datetime, timedelta, timezone
from typing import Any

from api.models import Message, Room

from django.test import TestCase


class RoomModelTest(TestCase):
    """Test constraints for the Room model."""

    @classmethod
    def setUpTestData(cls: Any) -> None:
        """Set up a static Room for all tests."""
        cls.digest, cls.slug = (
            'd894078911a34620ad24250222ddecb4',
            'seven-steak-pennsylvania-oregon'
        )
        Room.objects.create(
            uuid=cls.digest,
            slug=cls.slug
        )

    def test_uuid_max_length(self: TestCase) -> None:
        """Ensure that the max uuid length is 50 characters."""
        room = Room.objects.get(uuid=RoomModelTest.digest)
        max_length = room._meta.get_field('uuid').max_length
        self.assertEquals(max_length, 32)

    def test_slug_max_length(self: TestCase) -> None:
        """Ensure that the max slug length is 32 characters."""
        room = Room.objects.get(uuid=RoomModelTest.digest)
        max_length = room._meta.get_field('slug').max_length
        self.assertEquals(max_length, 50)

    def test_room_name_is_slug(self: TestCase) -> None:
        """Test that casting a Room to str will return its slug."""
        room = Room.objects.get(uuid=RoomModelTest.digest)
        self.assertEquals(str(room), RoomModelTest.slug)


class MessageModelTest(TestCase):
    """Test constraints for the Message model."""

    @classmethod
    def setUpTestData(cls: Any) -> None:
        """Set up a static Room and Message for all tests."""
        room = Room.objects.create(
            uuid='d894078911a34620ad24250222ddecb4',
            slug='seven-steak-pennsylvania-oregon'
        )
        cls.created_at = datetime.now(timezone.utc)
        Message.objects.create(
            pk=1,
            author='Kenobi',
            content='Hello there',
            room=room
        )

    def test_message_creation_date(self: TestCase) -> None:
        """Test that the Message creation date is accurate to the second."""
        message = Message.objects.get(pk=1)
        difference = message.time - MessageModelTest.created_at
        self.assertLess(
            difference, timedelta(seconds=1)
        )

    def test_author_max_length(self: TestCase) -> None:
        """Ensure that the max author length is 100 characters."""
        message = Message.objects.get(pk=1)
        max_length = message._meta.get_field('author').max_length
        self.assertEquals(max_length, 100)

    def test_content_max_length(self: TestCase) -> None:
        """Ensure that the max content length is 256 characters."""
        message = Message.objects.get(pk=1)
        max_length = message._meta.get_field('content').max_length
        self.assertEquals(max_length, 256)

    def test_message_name_is_content(self: TestCase) -> None:
        """Test that casting Messages to str will return 'author: content'."""
        message = Message.objects.get(pk=1)
        self.assertEquals(str(message), f'{message.author}: {message.content}')
