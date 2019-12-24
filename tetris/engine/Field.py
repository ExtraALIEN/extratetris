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
        self.active_piece = self.create_piece()
        self.websocket = None
        self.player = None
        self.speed = 0
        self.timer_speed = 3

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
        piece = ActivePiece(piece,
                            field=self,
                            x=self.width//2 - 1 + random.randint(-2, 2),
                            y=self.height-2)

        piece.fix_y()
        return piece

    def land_piece(self):
        for y in range(len(self.active_piece.shape)):
            for x in range(len(self.active_piece.shape[0])):
                if self.active_piece.shape[y][x] > 0:
                    self.surface[self.active_piece.y-y][x+self.active_piece.x] \
                        = self.active_piece.shape[y][x]
        terminated_lines = self.check_terminate()
        self.active_piece = self.create_piece()
        return len(terminated_lines) > 0

    def queue_to_view(self):
        return {x: self.queue.pieces[x].shape for x in range(len(self.queue.pieces))}

    def active_piece_to_view(self):
        return {'x': self.active_piece.x,
                'y': self.active_piece.y,
                'shape': self.active_piece.shape}

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
        self.timer_speed -= delay
        if self.timer_speed <= 0:
            self.speed += 1
            self.timer_speed += 3
            self.field_auto_move_down()
        print(self.timer_speed, self.speed)

        t = Timer(delay, self.update_timer, [delay])
        t.start()

    def field_auto_move_down(self):
        from engine.ingame import auto_move_down
        auto_move_down(self)
