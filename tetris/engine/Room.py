import asyncio
import websockets
from engine.Field import Field
from engine.ingame import process_command
from web.models import TetrisRoom


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

    def record_game(self):
        tetris_room = TetrisRoom.objects.get(room_id=self.id)
        print('guests: ', tetris_room.guests)
        tetris_room.delete()


    def finish_game(self):
        from engine.roomUtils import clear_room
        print('recording room')
        self.record_game()
        print('recorded')
        print('deleteing room')
        clear_room(self.id)
        print('deleted')

    def to_view(self):
        return {x : self.fields[x].to_view() for x in range(len(self.fields))}
