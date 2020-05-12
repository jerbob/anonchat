"""Websocket consumers."""

import json
from typing import Optional

from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer


class ChatConsumer(AsyncWebsocketConsumer):
    """Websocket consumer for chatrooms."""

    @database_sync_to_async
    def get_username(self: AsyncWebsocketConsumer) -> Optional[str]:
        """Get the username associated with the current session."""
        return self.scope['session']['username']

    async def connect(self: AsyncWebsocketConsumer) -> None:
        """Create a group for the user's session."""
        self.group_name = self.scope['url_route']['kwargs']['slug']

        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(
        self: AsyncWebsocketConsumer,
        close_code: int
    ) -> None:
        """Discard the user's group."""
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )

    async def receive(
        self: AsyncWebsocketConsumer,
        text_data: Optional[str] = None
    ) -> None:
        """Send a message event if we get a message."""
        if text_data is not None:
            data = json.loads(text_data)
            author = await self.get_username()
            content = data.get('content')
            if author and content:
                await self.channel_layer.group_send(
                    self.group_name,
                    {
                        'type': 'message',
                        'content': content,
                        'author': author
                    }
                )

    async def message(
        self: AsyncWebsocketConsumer,
        event: dict
    ) -> None:
        """Broadcast the message to connected clients."""
        content = event.get('content')
        author = event.get('author')

        await self.send(text_data=json.dumps({
            'content': content,
            'author': author,
        }))
