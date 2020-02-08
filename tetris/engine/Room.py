import asyncio
import websockets
from django.utils import timezone
from engine.Field import Field
from engine.ingame import process_command
from web.models import TetrisRoom, SingleGameRecord
from web.helpers import GAME_COUNTS, POWERUPS
from random import randint


class Room:
    def __init__(self, id, size, type):
        self.id = id
        self.type = type
        self.flag = False
        if self.type in ['CF', 'HF']:
            self.flag = True
        self.players = size
        self.fields = [Field(room=self, pos=i) for i in range(self.players)]
        self.start_time = None


    def start_timers(self):
        delay = .01
        self.start_time = timezone.now()
        for field in self.fields:
            field.update_timer(delay)
        if self.type in ['CF', 'HF']:
            self.reset_flag()

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
        eff_points = {}
        if self.players > 1:
            gap = 100 / (self.players - 1)
            next_eff = 100
            for x in sorted(places):
                bank = 0
                for y in places[x]:  #
                    bank += next_eff
                    next_eff -= gap
                eff_points[x] = bank/len(places[x])

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
                if field.max_speed > player.best_speed:
                    player.best_speed = field.max_speed
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
                        if field.pos in places[p]:
                            eff = eff_points[p]
                            break
                    player.effective_points += eff
                    prop = 'effective_points_' + GAME_COUNTS[self.type]
                    new_val = getattr(player, prop) + eff
                    setattr(player, prop, new_val)
                player.save()



    def record_game(self):
        final_places = self.detect_places()
        self.update_records(final_places)



    def finish_game(self):
        from engine.roomUtils import clear_room
        self.record_game()

        print('deleteing room')
        clear_room(self.id)
        tetris_room = TetrisRoom.objects.get(room_id=self.id)
        author = tetris_room.author
        tetris_room.delete()
        if author.is_guest:
            author.delete()
            print('guest deleted')
        print('deleted')

    def announce_powerup(self, pos, num, powerup=None, time=None):
        from engine.roomUtils import broadcast_room
        msg = {'type': 'powerup', 'pos' : pos, 'num': num + 1, 'powerup': powerup, 'time': time}
        broadcast_room(self.id, msg)

    def reset_flag(self):
        for field in self.fields:
            if self.flag:
                field.set_flag(5)

    def announce_flag(self, pos, y):
        from engine.roomUtils import broadcast_room
        msg = {'type': 'flag', 'pos' : pos, 'y': y}
        broadcast_room(self.id, msg)

    def move_flag(self, pos):
        y = self.fields[pos].flag_height
        for field in self.fields:
            if field.pos != pos:
                field.set_flag(y+1)
            else:
                field.set_flag(y-1)

    def give_flag(self, pos):
        for field in self.fields:
            if field.pos == pos:
                field.flag_hold = True
            else:
                field.flag_hold = False


    def unblind(self, pos, x):
        from engine.roomUtils import broadcast_room
        msg = { 'type': 'remove-blind',
                'pos': pos,
                'x': x
        }
        if x == 'queue':
            del msg['x']
        broadcast_room(self.id, msg)

    def fields_in_game(self):
        res = []
        for field in self.fields:
            if not field.game_over:
                res.append(field.pos)
        return res

    def execute_powerup(self, code, target, starter=None):
        from engine.roomUtils import broadcast_room
        if target not in self.fields_in_game() or self.fields[target].game_over:
            return 0
        powerup = POWERUPS[code]
        tg = self.fields[target]
        if tg.shield_time > 0:
            if powerup == 'shield':
                tg.shield_time += 45
            else:
                tg.shield_time -= 15
                if tg.shield_time < 0:
                    tg.shield_time = 0
            return 1
        msg = None
        if powerup == 'chance_up':
            tg.powerup_mul /= 0.75
        elif powerup == 'chance_down':
            tg.powerup_mul *= 0.75
        elif powerup == 'speed_up':
            tg.change_speed(10)
            msg =  {'type': 'update-tetris',
                    'pos' : tg.pos,
                    'speed': tg.speed,
                    'time': tg.time
                    }
        elif powerup == 'speed_down':
            tg.change_speed(-10)
            msg =  {'type': 'update-tetris',
                    'pos' : tg.pos,
                    'speed': tg.speed,
                    'time': tg.time
                    }
        elif powerup.startswith('line_add'):
            i = int(powerup[-1])
            for x in range(i):
                tg.add_line()
            msg = {'type': 'refresh-tetris',
                   'pos' : tg.pos,
                   'surface': tg.surface_to_view(),
                   'new_piece': tg.active_piece.to_view()
                  }
        elif powerup.startswith('line_remove'):
            i = int(powerup[-1])
            for x in range(i):
                tg.remove_line()
            msg = {'type': 'refresh-tetris',
                   'pos' : tg.pos,
                   'surface': tg.surface_to_view(),
                   'new_piece': tg.active_piece.to_view()
                  }
        elif powerup == 'copy_figure':
            piece = tg.active_piece
            tg.queue.fill(piece.color, piece.shape_number)
            msg = {'type': 'refresh-tetris',
                            'pos' : tg.pos,
                            'queue': tg.queue.to_view(),
                    }
        elif powerup == 'duration_up':
            tg.powerups_lifetime /= 0.8
            for x in tg.powerups_time:
                x /= 0.8
        elif powerup == 'duration_down':
            tg.powerups_lifetime *= 0.8
            for x in tg.powerups_time:
                x *= 0.8
        elif powerup == 'thunder':
            tg.put_thunder()
            msg = {'type': 'refresh-tetris',
                   'pos' : tg.pos,
                   'surface': tg.surface_to_view(),
                   'new_piece': tg.active_piece.to_view()
                  }
        elif powerup == 'shield':
            tg.shield_time += 45
        elif powerup == 'bomb':
            tg.put_bomb()
            msg = {'type': 'refresh-tetris',
                   'pos' : tg.pos,
                   'surface': tg.surface_to_view(),
                   'new_piece': tg.active_piece.to_view()
                  }
        elif powerup == 'trash':
            for x in range(3):
                tg.remove_powerup(x)
        elif powerup == 'blind':
            msg = {'type': 'blind',
                   'pos': tg.pos,
                   'cols': tg.set_blind()
                   }
        elif powerup == 'blind_queue':
            if tg.set_blind_queue():
                msg = {'type': 'blind',
                       'pos': tg.pos,
                      }
        elif powerup == 'drink':
            tg.drink_time += 20
        elif powerup == 'weak_signal':
            tg.weak_time += 20
            if tg.lost_actions == 0:
                tg.lost_actions = randint(0, 4)
        if msg is not None:
            broadcast_room(self.id, msg)
        return 1


    def to_view(self):
        return {x : self.fields[x].to_view() for x in range(len(self.fields))}
