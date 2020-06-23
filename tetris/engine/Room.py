import asyncio
import websockets
from django.utils import timezone
from engine.Field import Field
from engine.ingame import process_command
from web.models import TetrisRoom, SingleGameRecord
from web.helpers import GAME_COUNTS, POWERUPS, VOLUME_STANDARD
from random import randint


class Room:
    def __init__(self, id, size, type, proc):
        self.id = id
        self.type = type
        self.flag = False
        self.proc = proc
        if self.type in ['CF', 'HF']:
            self.flag = True
        self.players = size
        arg = {'room': self,
               }
        if self.type == 'CL':
            arg['powerup_mul'] = 0
        elif self.type == 'RA':
            arg['ra_next'] = 0
        if self.proc != 100:
            if self.type == 'LI':
                arg['max_lines'] = (proc*VOLUME_STANDARD['LI']) // 100
            elif self.type == 'CO':
                arg['timeleft'] = (proc*VOLUME_STANDARD['CO']) / 100
            elif self.type == 'SA':
                arg['score_finish'] = (proc*VOLUME_STANDARD['SA']) // 100
            elif self.type == 'DR':
                arg['drag_finish'] = (proc*VOLUME_STANDARD['DR']) // 100
            elif self.type == 'AC':
                arg['acc_finish'] = (proc*VOLUME_STANDARD['AC']) // 100

        self.fields = [Field(pos=i, **arg) for i in range(self.players)]
        self.start_time = None
        self.lines = 0
        self.next_positive = 5
        self.next_negative = 11
        self.next_negative2 = 14


    def human_players(self):
        s = self.players
        for field in self.fields:
            if field.websocket == 'bot':
                s -= 1
        return s


    def start_timers(self):
        delay = .01
        self.start_time = timezone.now()
        for field in self.fields:
            field.update_timer(delay)
            if field.websocket == 'bot':
                field.start_player.start()
        if self.type in ['CF', 'HF']:
            self.reset_flag()
        elif self.type == 'RA':
            self.announce_goals()
            self.announce_lines()

    def players_left(self):
        total = 0
        for field in self.fields:
            if not field.game_over:
                total += 1
        return total

    def update_ra_add(self, time):
        for field in self.fields:
            if not field.game_over:
                field.ra_next = time + 60
                field.ra_applied = False
                field.ra_add += 1

    def update_lines(self, pos, lines):
        self.lines += lines
        announce = False
        if self.lines >= self.next_positive:
            self.fields[pos].goal += 2
            if self.next_positive % 10 == 0:
                self.fields[pos].goal += 1
            if self.next_positive % 25 == 0:
                self.fields[pos].goal += 1
            if self.next_positive % 100 == 0:
                self.fields[pos].goal += 1
            self.next_positive += 5
            announce = True
        if self.lines >= self.next_negative:
            self.fields[pos].goal -= 1
            self.next_negative += 5
            announce = True
        if self.lines >= self.next_negative2:
            self.fields[pos].goal -= 1
            if (self.next_negative2 + 1) % 10 == 0:
                self.fields[pos].goal -= 1
            if (self.next_negative2 + 1) % 25 == 0:
                self.fields[pos].goal -= 1
            if (self.next_negative2 + 1) % 100 == 0:
                self.fields[pos].goal -= 1
            self.next_negative2 += 5
            announce = True
        self.announce_lines()
        if announce:
            self.announce_goals()


    def detect_places(self):
        from engine.roomUtils import broadcast_room
        results = {}  # res: [pos,]
        for field in self.fields:
            res = field.result
            pos = field.pos
            if res is None:
                if -9000 not in results:
                    results[-9000] = []
                results[-9000].append(pos)
            else:
                if res not in results:
                    results[res] = []
                results[res].append(pos)
        # print(results)
        places = sorted(results)
        # print(places)
        if self.type in ['CL', 'DM', 'SU', 'CO', 'CF', 'HF' ,'RA']:
            places = list(reversed(places))
        if -9000 in places and places[0] == -9000:
            tmp = places[0]
            places = places[1:]
            places.append(tmp)
        place = 0
        final = {}
        for x in places:
            place += 1
            final[place] = []
            if x != -9000:
                for p in results[x]:
                    final[place].append(p)
            place += len(final[place]) - 1
        if -9000 in places:
            place += 1
            for p in results[-9000]:
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
        stats = {}
        graphs = {}
        for field in self.fields:
            stat = field.game_stats_to_view()
            stat['username'] = field.start_player.username
            stats[field.pos] = stat
            graphs[field.pos] = field.graph

            if field.websocket != 'bot':
                player = field.start_player
                if not player.is_guest:
                    rec.players.add(player)
                    player.update_stats(type=self.type,
                                        rec=rec,
                                        multiplayer=self.players > 1,
                                        score=field.score,
                                        time=field.time,
                                        actions=field.actions,
                                        lines=field.lines,
                                        distance=field.distance,
                                        figures=field.total_figures,
                                        countdown_score=field.score_intermediate_st,
                                        time_lines=field.time_lines,
                                        time_drag=field.time_drag,
                                        time_climb=field.time_climb,
                                        time_acc=field.time_acc,
                                        max_speed=field.max_speed,
                                        games=1
                                        )

                    if self.players > 1:
                        eff = 0
                        for p in places:
                            if field.pos in places[p]:
                                eff = eff_points[p]
                                break
                        player.update_eff(self.type, eff)
                    player.save()
        rec.save_stats(stats)
        rec.save_graphs(graphs)

    def need_record(self):
        for field in self.fields:
            if field.websocket != 'bot' and not field.start_player.is_guest:
                return True
        return False

    def record_game(self):
        final_places = self.detect_places()
        if self.need_record():
            self.update_records(final_places)


    def finish_game(self, forced=False):
        from engine.roomUtils import clear_room, remove_fields_bots
        tetris_room = TetrisRoom.objects.get(room_id=self.id)
        author = tetris_room.author
        self.record_game()
        remove_fields_bots(self.id)
        clear_room(self.id)
        tetris_room.delete()
        if author.is_guest:
            author.delete()

    def announce_powerup(self, pos, num, powerup=None, time=None):
        from engine.roomUtils import broadcast_room
        msg = {'type': 'powerup', 'pos' : pos, 'num': num + 1, 'powerup': powerup, 'time': time}
        broadcast_room(self.id, msg)

    def reset_flag(self):
        self.announce_goals()
        for field in self.fields:
            if self.flag:
                field.set_flag(5)

    def announce_goals(self):
        from engine.roomUtils import broadcast_room
        goals = [field.goal for field in self.fields]
        msg = {'type': 'goal', 'goals': goals}
        broadcast_room(self.id, msg)

    def announce_flag(self, pos, y):
        from engine.roomUtils import broadcast_room
        msg = {'type': 'flag', 'pos' : pos, 'y': y}
        broadcast_room(self.id, msg)

    def announce_lines(self):
        from engine.roomUtils import broadcast_room
        msg = {'type': 'room-lines', 'lines' : self.lines}
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
            tg.drink_time += 15
        elif powerup == 'weak_signal':
            tg.weak_time += 15
            if tg.lost_actions == 0:
                tg.lost_actions = randint(0, 4)
        if msg is not None:
            broadcast_room(self.id, msg)
        msg_snd = {
            'type': 'powerup-sound',
            'pos': tg.pos,
            'file': powerup
        }
        broadcast_room(self.id, msg_snd)
        return 1


    def to_view(self):
        return {x : self.fields[x].to_view() for x in range(len(self.fields))}
