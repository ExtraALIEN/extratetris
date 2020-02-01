import asyncio
import websockets
from django.utils import timezone
from engine.Field import Field
from engine.ingame import process_command
from web.models import TetrisRoom, SingleGameRecord
from web.helpers import GAME_COUNTS


class Room:
    def __init__(self, id, size, type):
        self.id = id
        self.type = type
        self.players = size
        self.fields = [Field(room=self, pos=i) for i in range(self.players)]
        self.start_time = None


    def start_timers(self):
        delay = .01
        self.start_time = timezone.now()
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

        print('recording room')
        # print('guests: ', tetris_room.guests)
        print(places)
        eff_points = {}
        if self.players > 1:
            gap = 100 / (self.players - 1)
            next_eff = 100
            for x in sorted(places):
                bank = 0
                for y in x:  #
                    bank += next_eff
                    next_eff -= gap
                eff_points[x] = bank/len(x)

        rec = SingleGameRecord(type=self.type, started_at=self.start_time, size=self.players)
        results = {place:
                   [self.fields[pos].start_player.username for pos in places[place]]
                    for place in places}
        rec.save_results(results)
        for field in self.fields:
            player = field.start_player
            if not player.is_guest:
                rec.players.add(player)
                player.games_count += 1
                prop = 'games_count_' + GAME_COUNTS[self.type]
                new_val = getattr(player, prop) + 1
                setattr(player, prop, new_val)
                player.score += field.score
                if field.score > player.best_score:
                    player.best_score = field.score
                if field.score_intermediate and field.score_intermediate > player.best_countdown_score:
                    player.best_countdown_score = field.score_intermediate
                if not player.best_time_lines or field.time_lines and field.time_lines < player.best_time_lines:
                    player.best_time_lines = field.time_lines
                if not player.best_time_drag or field.time_drag and field.time_drag < player.best_time_drag:
                    player.best_time_drag = field.time_drag
                if not player.best_time_climb or field.time_climb and field.time_climb < player.best_time_climb:
                    player.best_time_climb = field.time_climb
                if not player.best_time_acc or field.time_acc and field.time_acc < player.best_time_acc:
                    player.best_time_acc = field.time_acc
                player.time += field.time
                if field.time > player.best_survival_time:
                    player.best_survival_time = field.time
                player.actions += field.actions
                player.lines += field.lines
                if field.lines >= player.best_lines_count:
                    player.best_lines_count = field.lines
                player.distance += field.distance
                if field.distance >= player.best_distance:
                    player.best_distance = field.distance
                player.figures += field.total_figures

                if self.players > 1:
                    player.multiplayer_games_count += 1
                    prop = 'multiplayer_games_count_' + GAME_COUNTS[self.type]
                    new_val = getattr(player, prop) + 1
                    setattr(player, prop, new_val)
                    eff = 0
                    for p in places:
                        if field.pos in p:
                            eff = eff_points[p]
                            break
                    player.effective_points += eff
                    prop = 'effective_points_' + GAME_COUNTS[self.type]
                    new_val = getattr(player, prop) + eff
                    setattr(player, prop, new_val)
                player.save()






        print('recorded')


    def record_game(self):
        final_places = self.detect_places()
        self.update_records(final_places)



    def finish_game(self):
        from engine.roomUtils import clear_room
        self.record_game()

        print('deleteing room')
        clear_room(self.id)
        tetris_room = TetrisRoom.objects.get(room_id=self.id)
        tetris_room.delete()
        print('deleted')

    def to_view(self):
        return {x : self.fields[x].to_view() for x in range(len(self.fields))}
