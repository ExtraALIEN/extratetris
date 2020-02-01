import asyncio
import websockets
from engine.Field import Field
from engine.ingame import process_command
from web.models import TetrisRoom


class Room:
    def __init__(self, id, size, type):
        self.id = id
        self.type = type
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

    def detect_places(self):
        from engine.roomUtils import broadcast_room
        results = {}  # res: [pos,]
        for field in self.fields:
            res = field.result
            pos = field.pos
            if res is None:
                if -1 not in results:
                    results[-1] = []
                results[-1].append(pos)
            else:
                if res not in results:
                    results[res] = []
                results[res].append(pos)
        # print(results)
        places = sorted(results)
        # print(places)
        if self.type in ['CL', 'DM', 'SU', 'CO', 'CF', 'RA']:
            places = list(reversed(places))
        if -1 in places and places[0] == -1:
            tmp = places[0]
            places = places[1:]
            places.append(tmp)
        place = 0
        final = {}
        for x in places:
            place += 1
            final[place] = []
            if x != -1:
                for p in results[x]:
                    final[place].append(p)
            place += len(final[place]) - 1
        if -1 in places:
            place += 1
            for p in results[-1]:
                final[place].append(p)
        msg = {'type': 'places', 'places': final}
        broadcast_room(self.id, msg)
        return final

    def update_records(self, places):
        print(places)


    def record_game(self):
        tetris_room = TetrisRoom.objects.get(room_id=self.id)
        print('guests: ', tetris_room.guests)
        final = self.detect_places()
        print('recording room')
        self.update_records(final)
        print('recorded')
        tetris_room.delete()


    def finish_game(self):
        from engine.roomUtils import clear_room
        self.record_game()

        print('deleteing room')
        clear_room(self.id)
        print('deleted')

    def to_view(self):
        return {x : self.fields[x].to_view() for x in range(len(self.fields))}
