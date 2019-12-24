import asyncio
import websockets
from engine.Field import Field
from engine.ingame import process_command



class Room:
    def __init__(self, players):
        self.fields = [Field(room=self) for i in range(players)]

    def start_timers(self, id):
        print('start timers')
        delay = 1
        for field in self.fields:
            field.update_timer(delay)
