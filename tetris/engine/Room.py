import asyncio
import websockets
from engine.Field import Field
from engine.ingame import process_command



class Room:
    def __init__(self, players):
        self.fields = [Field(room=self, pos=i) for i in range(players)]

    def start_timers(self, id):
        print('start timers')
        delay = .01
        for field in self.fields:
            field.update_timer(delay)

    def to_view(self):
        return {x : self.fields[x].to_view() for x in range(len(self.fields))}
