from engine.ListMethods import buildEmptyFieldList
from engine.QueuePieces import QueuePieces
from engine.ActivePiece import ActivePiece
from threading import Timer
from random import randint, shuffle, choices, random

class Field:

    def __init__(self, pos, room=None,
                            width=12,
                            height=25,
                            acc_finish=100, #100
                            drag_finish=4020, #4020
                            timeleft=360, #360
                            score_finish=15000, #15000
                            max_lines=60): #60
        self.pos = pos
        self.room = room
        self.width = width
        self.height = height
        self.websocket = None
        self.player = None
        self.start_player = None
        self.speed = 0
        self.speed_boost = 0.02
        self.powerup_chance = 0.02
        self.powerup_boost = 0
        self.powerup_mul = 10
        self.powerups = [None, None, None]
        self.powerups_time = [0, 0, 0]
        self.powerups_lifetime = 15
        self.shield_time = 0
        self.max_speed = 0
        self.multiplier = 1
        self.to_movedown = 25 / (self.speed + 25)
        self.to_accelerate = 1.2
        self.total_figures = 0
        self.actions = 0
        self.lines = 0
        self.max_lines = max_lines
        self.time_lines = None
        self.score = 0
        self.time = 0
        self.distance = 0
        self.time_climb = None
        self.score_finish = score_finish
        self.score_intermediate = None
        self.timeleft = timeleft
        self.time_acc = None
        self.acc_finish = acc_finish
        self.time_drag = None
        self.drag_finish = drag_finish
        self.goal = 0
        self.surface = buildEmptyFieldList(width, height)
        self.queue = QueuePieces(pos=self.pos)
        self.active_piece = self.create_piece()
        self.game_over = False
        self.result = None

    def top_points(self):
        def top_point(x):
            for y in range(self.height-1, -1, -1):
                if self.surface[y][x] > 0:
                    return y+1
            return 0
        return [top_point(x) for x in range(self.width)]

    def create_piece(self):
        import random
        piece = self.queue.release_next_piece((self.powerup_chance+self.powerup_boost)*self.powerup_mul)
        piece = ActivePiece(piece,
                            field=self,
                            x=self.width//2 - 1 + random.randint(-2, 2),
                            y=self.height-2)
        piece.fix_y()
        if piece.blocked():
            from engine.roomUtils import broadcast_room
            upd = {'type': 'update-tetris',
                    'pos' : self.pos,
                    'current_piece': piece.to_view(),
                    'speed': self.speed,
                    'time': self.time,
                    'score': self.score,
                    'distance': self.distance
                    }
            broadcast_room(self.room.id, upd)
            self.end_game()
        self.total_figures += 1
        return piece

    def land_piece(self):
        for y in range(len(self.active_piece.shape)):
            for x in range(len(self.active_piece.shape[0])):
                if self.active_piece.shape[y][x] > 0:
                    self.surface[self.active_piece.y-y][x+self.active_piece.x] \
                        = self.active_piece.shape[y][x]
        terminated_lines = self.check_terminate()
        self.lines += len(terminated_lines)
        if sum(self.surface[-1]) > 0:
            self.end_game()
        else:
            self.add_score(terminated_lines)

        if not self.game_over:
            self.active_piece = self.create_piece()
            return len(terminated_lines) > 0


    def change_speed(self, delta):
        self.speed += delta
        if self.speed > self.max_speed:
            self.max_speed = self.speed
        elif self.speed < 0:
            self.speed = 0.02

    def add_line(self):
        filled = randint(self.width/2, self.width-1)
        cells = [x for x in range(self.width)]
        shuffle(cells)
        line = [0 for x in range(self.width)]
        for x in cells[:filled]:
            line[x] = randint(1, 8)
        self.surface.pop(-1)
        self.surface.insert(0, line)
        if self.active_piece.blocked():
            self.active_piece.y += 1


    def remove_line(self):
        self.surface.pop(0)
        self.surface.append([0 for x in range(self.width)])
        if self.active_piece.blocked():
            down = self.active_piece.bottom_points()
            for x in down:
                if down[x] == 0:
                    self.land_piece()
                    return
            self.active_piece.y -= 1


    def add_score(self, terminated_lines):
        import math

        def round_half_up(n):
            return math.floor(n + 0.5)

        lines = terminated_lines[::-1]
        base = 0
        mul = 1
        boost = 0
        powerup_boost = 0
        if len(lines) > 0:
            LINE_SCORES = [100, 300, 600, 1000]
            MUL_INCREASE = [1.05, 1.15, 1.25, 1.35]
            SPEED_BOOST = [0.3, 0.8, 1.5, 2.4]
            POWERUP_BOOSTS = [0.05, 0.13, 0.22, 0.33]
            combos = []
            row_numbers = []
            for x in range(len(lines)):
                if x == 0:
                    combos.append(1)
                    row_numbers.append(lines[x])
                else:
                    if lines[x] - 1 == lines[x-1]:
                        combos[-1] += 1
                    else:
                        combos.append(1)
                        row_numbers.append(lines[x])
            for x in combos:
                mul *= MUL_INCREASE[x-1]
                boost += SPEED_BOOST[x-1]
                powerup_boost += POWERUP_BOOSTS[x-1]
            for x in range(len(row_numbers)):
                base += LINE_SCORES[combos[x]-1]*(1 + (row_numbers[x] * (7 / 60)))
        else:
            self.multiplier = 1
            land_y = self.active_piece.detect_landing_row()
            base = 15 * (1 + (land_y * (7 / 60)))
        to_add = round_half_up(base * (math.sqrt(2)**(self.speed/50))*self.multiplier)
        self.score += to_add
        if self.score >= self.score_finish and self.time_climb is None:
            self.time_climb = self.time
            if self.room.type == 'SA':
                self.end_game()
        if self.lines >= self.max_lines and self.time_lines is None:
            self.time_lines = self.time
            if self.room.type == 'LI':
                self.end_game()

        self.powerup_boost = powerup_boost*self.multiplier
        self.multiplier *= mul
        self.change_speed(boost)

    def save_powerup(self, powerup_code):
        for x in range(3):
            if self.powerups[x] is None:
                self.powerups[x] = powerup_code // 100
                self.powerups_time[x] = self.powerups_lifetime
                self.room.announce_powerup(self.pos, x, powerup=(powerup_code // 100), time=self.powerups_time[x])
                return
        self.room.execute_powerup((powerup_code//100)-1, self.pos)

    def send_powerup_time(self, x, control_time):
        self.room.announce_powerup(self.pos, x, time=control_time)

    def remove_powerup(self, x):
        self.powerups[x] = None
        self.powerups_time[x] = 0
        self.room.announce_powerup(self.pos, x)

    def check_powerup(self, line):
        powerups = []
        for x in line:
            if x > 100:
                powerups.append(x)
        if len(powerups) > 0:
            return powerups

    def use_powerup(self, place, target, manual=False):
        pos = place - 1
        if self.powerups[pos] is not None:
            powerup_code = self.powerups[pos]
            result = self.room.execute_powerup(powerup_code-1, target-1, starter=self)
            if result == 1:
                self.remove_powerup(pos)
                if manual:
                    self.actions += 1

    def put_thunder(self):
        top = self.top_points()
        xs = [x for x in range(self.width)]
        weights = [x**6 for x in top]
        x = choices(xs, weights=weights)[0]
        prob = 1
        y = top[x]
        reduced = False
        while not reduced:
            if random() < prob or random() < prob or random() < prob:
                self.surface[y][x] = 0
                y -= 1
                if y < 0:
                    reduced = True
                elif self.surface[y][x] == 0:
                    prob -= 0.02
                else:
                    prob -= 0.08
                    if random() < 0.25:
                        if x == 0:
                            x += 1
                        elif x == self.width-1:
                            x -= 1
                        elif random() < 0.5:
                            x += 1
                        else:
                            x -= 1

            else:
                reduced = True

    def put_bomb(self):
        top = self.top_points()
        wing = 2
        center = randint(0, self.width-1)
        left_wing = wing
        right_wing = wing
        if center < wing:
            left_wing = center
            right_wing = 2 * wing - left_wing
        elif center > self.width-1-wing:
            right_wing = self.width-1-center
            left_wing = 2 * wing - right_wing
        top_y = top[center]
        bottom_y = top_y - 4
        if bottom_y < 0:
            bottom_y = 0
        top_side = {}
        for x in range(self.width):
            if not (center - left_wing <= x <= center + right_wing):
                 top_side[x] = top[x]
        bank = []
        width = [0, 0, 1, 2]
        w = 0
        for y in range(top_y, bottom_y, -1):
            print
            for x in range(center - left_wing + width[w], center + right_wing + 1 - width[w]):
                if self.surface[y][x] > 0:
                     bank.append(self.surface[y][x])
                     self.surface[y][x] = 0
            w += 1
        lands = [3, -3, 4, -4, 5, -5, 6, -6, 7, -7, 8, -8]
        c = 0
        while len(bank) > 0:
            x = center + lands[c]
            if x in top_side:
                self.surface[top_side[x]][x] = bank.pop(0)
                top_side[x] += 1
                if self.active_piece.blocked():
                    self.land_piece()
            c += 1
            if c == len(lands):
                c = 0




    def check_terminate(self):
        lines = []
        powerups = []
        for y in range(self.height-1, -1, -1):
            full = True
            for x in self.surface[y]:
                if x == 0:
                    full = False
                    break
            if full:
                lines.append(y)
                added_powerups = self.check_powerup(self.surface[y])
                if added_powerups is not None:
                    powerups.extend(added_powerups)
        for y in lines:
            self.surface.pop(y)
            self.surface.append([0 for x in range(self.width)])
        if len(powerups) > 0:
            shuffle(powerups)
            for x in powerups:
                self.save_powerup(x)
        return lines


    def move(self, command):
        from engine.ListMethods import diff_obj
        from engine.roomUtils import broadcast_room
        import engine.status as status
        id = status.connections[self.websocket]['id']
        piece = self.active_piece
        prev = piece.to_view()
        terminated = False
        prev_score = self.score
        prev_distance = self.distance
        if command == 'move_left':
            self.active_piece.move_left()
            self.actions += 1
        elif command == 'move_right':
            self.active_piece.move_right()
            self.actions += 1
        elif command == 'move_down':
            terminated = self.active_piece.move_down()
            self.change_speed(self.speed_boost)
            self.actions += 1
        elif command == 'auto_move_down':
            terminated = self.active_piece.move_down()
        elif command == 'rotate':
            self.active_piece.rotate()
            self.actions += 1
        if not self.game_over:
            cur = piece.to_view()
            piece_move = diff_obj(prev, cur)
            upd =  {'type': 'update-tetris',
                    'pos' : self.pos,
                    'current_piece': piece_move,
                    'speed': self.speed,
                    'time': self.time
                    }
            if self.score != prev_score:
                upd['score'] = self.score
            if self.distance != prev_distance:
                upd['distance'] = self.distance
            if terminated:
                upd['lines'] = self.lines
            broadcast_room(id, upd)
            after_piece = self.active_piece
            if after_piece is not piece:
                new_piece = after_piece.to_view()
                new_piece_copy = after_piece.to_view()
                for y in new_piece_copy:
                    if isinstance(y, int):
                        for x in new_piece_copy[y]:
                            if new_piece_copy[y][x] == 0:
                                del new_piece[y][x]
                queue = self.queue.to_view()
                refresh_field = {'type': 'refresh-tetris',
                                'pos' : self.pos,
                                'new_piece': new_piece,
                                'queue': queue}
                if terminated:
                    refresh_field['surface'] = self.surface_to_view()

                broadcast_room(id, refresh_field)



    def update_timer(self, delay):
        t = Timer(delay, self.update_timer, [delay])
        if not self.game_over:
            self.time += delay
            if self.speed >= self.acc_finish and self.time_acc is None:
                self.time_acc = self.time
                if self.room.type == 'AC':
                    self.end_game()
            if self.distance >= self.drag_finish and self.time_drag is None:
                self.time_drag = self.time
                if self.room.type == 'DR':
                    self.end_game()
            if self.time >= self.timeleft and self.score_intermediate is None:
                self.score_intermediate = self.score
                if self.room.type == 'CO':
                    self.end_game()
            self.to_movedown -= delay
            if self.to_movedown <= 0:
                self.auto_move_down()
                self.to_movedown += 12 / (self.speed + 12)
            for x in range(3):
                if self.powerups_time[x] > 0:
                    self.powerups_time[x] -= delay
                    if self.powerups[x] is not None:
                        if self.powerups_time[x] <= 0:
                            self.use_powerup(x+1, self.pos+1)
                        else:
                            for i in [3,6,9,12]:
                                if i-delay/2 < self.powerups_time[x] < i+delay/2:
                                    self.send_powerup_time(x, i)
                                    break
            if self.shield_time > 0:
                self.shield_time -= delay

            self.to_accelerate -= delay
            if self.to_accelerate <= 0:
                self.speed += .1
                if self.speed > self.max_speed:
                    self.max_speed = self.speed
                self.to_accelerate += 1.2
            t.start()
        else:
            t.cancel()


    def auto_move_down(self):
        if not self.game_over:
            self.move('auto_move_down')


    def end_game(self, hard_disconnect=False):

        print('end game')
        self.game_over = True
        hard = False
        if hard_disconnect:
            print('                   HARD DISCONNECT')
            hard = True
        self.broadcast_gameover(hard)
        print('                          game over')
        print('left ', self.room.players_left())
        if self.room.players_left() == 0:
            self.room.finish_game()

    def game_stats_to_view(self):
        from web.helpers import TYPE_OF_RESULT
        stats = {'time' : self.time,
               'score' : self.score,
               'lines': self.lines,
               'distance': self.distance,
               'score-sec': self.score/self.time,
               'lines-min': self.lines/(self.time/60),
               'apm': self.actions/(self.time/60),
               'actions-piece': self.actions/self.total_figures,
               'score-piece': self.score/self.total_figures,
               'pieces': self.total_figures,
               'pieces-min': self.total_figures/(self.time/60),
               'max-speed': self.max_speed,
                }
        if self.lines > 0:
            stats['pieces-line'] = self.total_figures/self.lines
            stats['dist-line'] = self.distance/self.lines
        if self.distance > 0:
            stats['score-dist'] = self.score/self.distance
        if self.actions > 0:
            stats['score-action'] = self.score/self.actions
        if self.time_acc is not None:
            stats['time-acc'] = self.time_acc
        if self.time_lines is not None:
            stats['time-lines'] = self.time_lines
        if self.time_drag is not None:
            stats['time-drag'] = self.time_drag
        if self.time_climb is not None:
            stats['time-climb'] = self.time_climb
        if self.score_intermediate is not None:
            stats['score-intermediate'] = self.score_intermediate

        x = TYPE_OF_RESULT[self.room.type]
        self.result = getattr(self, x)
        stats['result'] = self.result
        return stats

    def broadcast_gameover(self, hard_disconnect):
        from engine.roomUtils import broadcast_room
        msg = {'type': 'game-over',
               'mode': self.room.type,
               'pos': self.pos,
               'stats': self.game_stats_to_view(),
               'disconnect': hard_disconnect}
        print('broadcasting gameover')
        broadcast_room(self.room.id, msg)

    def surface_to_view(self):
        obj = {y:
               {x: self.surface[y][x] for x in range(self.width)}
               for y in range(self.height-1)}
        obj['pos'] = self.pos
        return obj

    def to_view(self):
        return {
            'speed': self.speed,
            'lines': self.lines,
            'score': self.score,
            'time': self.time,
            'distance': self.distance,
            'surface': self.surface_to_view(),
            'queue': self.queue.to_view(),
            'active_piece':self.active_piece.to_view()
        }
