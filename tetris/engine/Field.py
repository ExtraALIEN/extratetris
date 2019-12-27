from engine.ListMethods import buildEmptyFieldList
from engine.QueuePieces import QueuePieces
from engine.ActivePiece import ActivePiece
from threading import Timer

class Field:

    def __init__(self, pos, room=None, width=12, height=25, ):
        self.pos = pos
        self.room = room
        self.width = width
        self.height = height
        self.websocket = None
        self.player = None
        self.speed = 0
        self.speed_boost = 0.02
        self.multiplier = 1
        self.to_movedown = 25 / (self.speed + 25)
        self.to_accelerate = 1.2
        self.total_figures = 0
        self.lines = 0
        self.score = 0
        self.time = 0
        self.distance = 0
        self.surface = buildEmptyFieldList(width, height)
        self.queue = QueuePieces(pos=self.pos)
        self.active_piece = self.create_piece()
        self.game_over = False

    def top_points(self):
        def top_point(x):
            for y in range(self.height):
                if self.surface[y][x] > 0:
                    return y
            return 0
        return [top_point(x) for x in range(self.width)]

    def create_piece(self):
        import random
        piece = self.queue.release_next_piece()
        self.total_figures += 1
        piece = ActivePiece(piece,
                            field=self,
                            x=self.width//2 - 1 + random.randint(-2, 2),
                            y=self.height-2)
        piece.fix_y()
        if piece.blocked():
            self.end_game()
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

        print('pieces: ', self.total_figures, ' lines: ', self.lines,'dist: ', self.distance, ' score: ', self.score )
        if not self.game_over:
            self.active_piece = self.create_piece()
            return len(terminated_lines) > 0


    def add_score(self, terminated_lines):
        import math

        def round_half_up(n):
            return math.floor(n + 0.5)

        lines = terminated_lines[::-1]
        base = 0
        mul = 1
        if len(lines) > 0:
            LINE_SCORES = [100, 300, 600, 1000]
            MUL_INCREASE = [1.05, 1.15, 1.25, 1.35]
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
            print(combos)
            for x in combos:
                mul *= MUL_INCREASE[x-1]
            for x in range(len(row_numbers)):
                base += LINE_SCORES[combos[x]-1]*(1 + (row_numbers[x] * (7 / 60)))
        else:
            self.multiplier = 1
            land_y = self.active_piece.detect_landing_row()
            base = 15 * (1 + (land_y * (7 / 60)))
        print( 'mul: ', self.multiplier )
        to_add = round_half_up(base * (math.sqrt(2)**(self.speed/50))*self.multiplier)
        print('to add: ', to_add)
        self.score += to_add
        self.multiplier *= mul


    def check_terminate(self):
        lines = []
        for y in range(self.height-1, -1, -1):
            full = True
            for x in self.surface[y]:
                if x == 0:
                    full = False
                    break
            if full:
                lines.append(y)
        for y in lines:
            self.surface.pop(y)
            self.surface.append([0 for x in range(self.width)])
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
        elif command == 'move_right':
            self.active_piece.move_right()
        elif command == 'move_down':
            terminated = self.active_piece.move_down()
            self.speed += self.speed_boost
        elif command == 'auto_move_down':
            terminated = self.active_piece.move_down()
        elif command == 'rotate':
            self.active_piece.rotate()
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
        self.time += delay
        self.to_movedown -= delay
        if self.to_movedown <= 0:
            self.auto_move_down()
            self.to_movedown += 25 / (self.speed + 25)
        self.to_accelerate -= delay
        if self.to_accelerate <= 0:
            self.speed += .1
            self.to_accelerate += 1.2
        t = Timer(delay, self.update_timer, [delay])
        if not self.game_over:
            t.start()
        else:
            print('time at field: ', self.time)

    def auto_move_down(self):
        self.move('auto_move_down')

    def end_game(self, hard_disconnect=False):
        self.game_over = True
        if hard_disconnect:
            print('                   HARD DISCONNECT')
        print('                          game over')
        print('left ', self.room.players_left())
        if self.room.players_left() == 0:
            pass



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
