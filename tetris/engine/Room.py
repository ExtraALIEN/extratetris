import asyncio
import websockets
from engine.Field import Field
from engine.ingame import process_command



class Room:
    def __init__(self, id, size):
        self.id = id
        self.players = size
        self.fields = [Field(room=self, pos=i) for i in range(self.players)]


    def start_timers(self):
        delay = .01
        for field in self.fields:
            field.update_timer(delay)

    def players_left(self):
        total = 0
        for field in self.fields:
            if not field.game_over:
                total += 1
        return total

    def finish_game(self):
        print('finish', self.id)

    def to_view(self):
        return {x : self.fields[x].to_view() for x in range(len(self.fields))}
