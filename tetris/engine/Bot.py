from threading import Timer
from random import choice

class Bot:
    def __init__(self, room, pos):
        self.username = '* bot *'
        self.room = room
        self.pos = pos
        self.field = room.fields[pos]
        self.delay = .01
        self.speed = 40
        self.to_next_action = 1.01 - (0.01*self.speed)
        self.current_max = 0
        self.target = []
        self.locked_target = False
        self.checked_target = False
        self.rotates = 0
        self.best_rotate = 0
        self.prev_piece = self.field.active_piece

    def start(self):
        self.update_timer(self.delay)

    def update_timer(self, delay):
        t = Timer(delay, self.update_timer, [delay])
        if not self.field.game_over:
            self.to_next_action -= delay
            if self.to_next_action <= 0:
                self.to_next_action += 1.01 - (0.01*self.speed)
                self.next_action()
            t.start()
        else:
            t.cancel()

    def next_action(self):
        if self.field.active_piece is not self.prev_piece:
            self.next_piece()
        if not self.locked_target:
            self.detect_target()
        else:
            self.move_to_target()


    def detect_target(self):
        piece = self.field.active_piece
        phantom = piece.make_phantom()
        while not self.locked_target:
            if not self.checked_target:
                shape = phantom.trimmed_shape()
                possible_land = phantom.detect_possible_landing_height(shape)
                base = possible_land
                points = [self.field.height-(sum(x)/len(x)) for x in base]
                max_points = max(points)
                if max_points > self.current_max:
                    self.current_max = max_points
                    self.best_rotate = self.rotates % 4
                    target = []
                    for x in range(len(points)):
                        if points[x] == max_points:
                            x_offset = self.detect_offset(phantom.shape)
                            print('offset ', x_offset)
                            target.append(x + x_offset)
                    self.target = target
                phantom.rotate()
                self.rotates += 1
                if self.rotates >= 4:
                    self.checked_target = True
                    self.rotates = 0
            else:
                self.target = choice(self.target)
                self.locked_target = True


    def move_to_target(self):
        piece = self.field.active_piece
        command = 'move_'
        if self.rotates % 4 != self.best_rotate:
            command = 'rotate'
            self.rotates += 1
        else:
            if piece.x > self.target:
                command += 'left'
            elif piece.x < self.target:
                command += 'right'
            else:
                command += 'down'
        self.field.move(command)

    def rotate(self):
        self.field.move('rotate')

    def next_piece(self):
        self.prev_piece = self.field.active_piece
        self.current_max = 0
        self.target = []
        self.locked_target = False
        self.checked_target = False
        self.rotates = 0

    def detect_offset(self, trimmed_shape):
        for y in range(len(trimmed_shape)):
            if trimmed_shape[y][0] > 0:
                return 0
        return -1
