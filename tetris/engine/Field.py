from engine.ListMethods import buildEmptyFieldList
from engine.QueuePieces import QueuePieces
from engine.ActivePiece import ActivePiece
from threading import Timer

class Field:

    def __init__(self, room=None, width=12, height=25, ):
        self.room = room
        self.width = width
        self.height = height
        self.surface = buildEmptyFieldList(width, height)
        self.queue = QueuePieces()
        self.websocket = None
        self.player = None
        self.speed = 0
        self.speed_boost = 0.02
        self.to_movedown = 25 / (self.speed + 25)
        self.to_accelerate = 1.2
        self.total_figures = 0
        self.lines = 0
        self.score = 0
        self.time = 0
        self.distance = 0
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
        if len(lines) > 0:
            LINE_SCORES = [100, 300, 600, 1000]
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
            for x in range(len(row_numbers)):
                base += LINE_SCORES[combos[x]-1]*(1 + (row_numbers[x] * (7 / 60)))
        else:
            land_y = self.active_piece.detect_landing_row()
            base = 15 * (1 + (land_y * (7 / 60)))
        to_add = round_half_up(base * (math.sqrt(2)**(self.speed/50)))
        print('to add: ', to_add )
        self.score += to_add


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


    def update_timer(self, delay):
        self.time += delay
        self.to_movedown -= delay
        if self.to_movedown <= 0:
            self.field_auto_move_down()
            self.to_movedown += 25 / (self.speed + 25)
        self.to_accelerate -= delay
        if self.to_accelerate <= 0:
            self.speed += .1
            self.to_accelerate += 1.2
            print('speed', self.speed)
        t = Timer(delay, self.update_timer, [delay])
        if not self.game_over:
            t.start()
        else:
            print('game over')

    def field_auto_move_down(self):
        from engine.ingame import auto_move_down
        auto_move_down(self)

    def end_game(self):
        self.game_over = True
