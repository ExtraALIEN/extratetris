import asyncio
import websockets
from engine.Field import Field


class Room:
    def __init__(self, players):
        self.fields = [Field(room=self) for i in range(players)]

    def send_start(self):
        pass
