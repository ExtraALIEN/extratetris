import asyncio
import websockets
from Field import Field


class Room:
    def __init__(self, players):
        self.fields = [Field(room=self) for i in players]

    def send_start(self):
        pass
