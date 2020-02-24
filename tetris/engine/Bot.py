from threading import Timer
from random import choice

class Bot:
    def __init__(self, room, pos):
        self.username = '* bot *'
        self.room = room
        self.pos = pos
        self.field = room.fields[pos]
        self.delay = .01
        self.skill = 50
        self.speed = 86
        self.mul_land = 3
        self.mul_clean = 5
        self.mul_reach = 8
        self.mul_side = 2
        self.mul_height = 5
        self.mul_lines = 6
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
                top = self.field.top_points()
                possible_land = phantom.detect_possible_landing_height(shape, top)
                base = possible_land
                points = self.sum_points(self.land_points(base),
                                         self.clean_points(base),
                                         self.reach_points(base),
                                         self.side_points(base, shape),
                                         self.height_points(base, shape, max(top)),
                                         self.line_points(base, shape))
                # print(points)
                max_points = max(points)
                if max_points > self.current_max:
                    self.current_max = max_points
                    self.best_rotate = self.rotates % 4
                    target = []
                    for x in range(len(points)):
                        if points[x] == max_points:
                            x_offset = self.detect_offset(phantom.shape)
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

    def land_points(self, base):
        result = [ ((self.field.height-sum(x)/len(x))/self.field.height) * 100 for x in base]
        result = [x*self.mul_land for x in result]
        return result

    def clean_points(self, base):
        width = len(base[0])
        spaces = []
        for x in range(len(base)):
            closed = 0
            for dx in range(width):
                y = base[x][dx]
                if y > 0 and self.field.surface[y-1][x+dx] == 0:
                    closed += 1
                    for yy in range(y-1, -1, -1):
                        if self.field.surface[yy][x+dx] == 0:
                            closed += 1
                        else:
                            break
            spaces.append(closed)
        result = [((self.field.height - x)/self.field.height)*100 for x in spaces]
        result = [x*self.mul_clean for x in result]
        return result

    def reach_points(self, base):
        piece = self.field.active_piece
        height = len(list(filter(lambda a: sum(a) > 0, piece.shape)))
        cur_y = piece.y - len(piece.shape) + height
        width = len(base[0])

        result = []
        for x in range(len(base)):
            blocked = set()
            for dx in range(width):
                if dx not in blocked:
                    target_y = base[x][dx] + height
                    for y in range(target_y, cur_y):
                        if self.field.surface[y][x+dx] > 0:
                            blocked.add(dx)

            result.append( ((width - len(blocked))/width)*100 )

        result = [x*self.mul_reach for x in result]
        return result

    def side_points(self, base, shape):

        height = len(shape)
        width = len(shape[0])
        result = []
        for x in range(len(base)):
            baseline = min(base[x])
            total_sides = 0
            connected_sides = 0
            land_y = baseline + height - 1
            for y in range(height):
                for dx in range(width):
                    if shape[y][dx]:
                        total_sides += 1
                        if x+dx-1 < 0:
                            connected_sides += 1
                        elif self.field.surface[land_y-y][x+dx-1] > 0:
                            connected_sides += 1
                        break
                for dx in range(width-1, -1, -1):
                    if shape[y][dx]:
                        total_sides += 1
                        if x+dx+1 > self.field.width-1:
                            connected_sides += 1
                        elif self.field.surface[land_y-y][x+dx+1] > 0:
                            connected_sides += 1
                        break
            result.append( (connected_sides/total_sides) * 100)
        result = [x*self.mul_side for x in result]
        return result


    def height_points(self, base, shape, t):
        height = len(shape)
        result = [  (max((self.field.height-(min(x)+height)),t) /
                    (self.field.height-1))*100 for x in base]
        result = [x*self.mul_height for x in result]
        return result


    def line_points(self, base, shape):
        height = len(shape)
        result = []
        for x in range(len(base)):
            baseline = min(base[x])
            land_y = baseline + height - 1
            lines = 0
            for y in range(height):
                cells = len(list(filter(lambda a: a > 0, shape[y])))
                spaces = len(list(filter(lambda a: a == 0, self.field.surface[land_y-y])))
                if cells == spaces:
                    lines += 1
            result.append(lines*25)
        result = [x*self.mul_lines for x in result]
        return result


    def sum_points(self, *args):
        return [sum(x) for x in zip(*args)]
