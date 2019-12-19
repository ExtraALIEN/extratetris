import asyncio
import json
from channels.consumer import AsyncConsumer
from channels.db import database_sync_to_async

class WsConsumer(AsyncConsumer):
    async def websocket_connect(self, event):
        print("connected", event)
        await self.send({
            'type': 'websocket.accept',

        })
        await asyncio.sleep(4)
        await self.send({
            'type': 'websocket.send',
            'text': 'hello'

        })

    async def websocket_receive(self, event):
        print("receive", event)

    async def websocket_disconnect(self, event):
        print("disconnected", event)
