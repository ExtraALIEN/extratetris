from engine.Piece import Piece
from web.helpers import VOLUME_STANDARD

class ActivePiece(Piece):
    def __init__(self, current_piece, x, y, field):
        self.color = current_piece.color
        self.shape = current_piece.shape
        self.shape_number = current_piece.shape_number
        self.x = x
        self.y = y
        self.field = field


    def fix_y(self):
        if sum(self.shape[0]) == 0:
            self.y += 1

    def make_phantom(self):
        current_piece = Piece()
        current_piece.shape = self.shape
        phantom = ActivePiece(x=self.x,
                              y=self.y,
                              current_piece=current_piece,
                              field=self.field)
        return phantom


    def bottom_points(self):
        def bottom_point(x):
            if x+self.x >= self.field.width:
                return -1
            for y in range(len(self.shape)-1, -1, -1):
                if self.shape[y][x] != 0:
                    return self.y-y
            return -1
        points = {x+self.x: bottom_point(x) for x in range(len(self.shape[0]))}
        result = {}
        for x in points:
            if points[x] != -1:
                result[x] = points[x]
        return result


    def detect_landing_row(self):
        land_y = None
        points = self.bottom_points()
        has_zero = False
        for x in points:
            y = points[x]
            if y > 0:
                if self.field.surface[y-1][x] > 0:
                    if land_y is None:
                        land_y = y
                    elif y < land_y:
                        land_y = y
            elif y == 0:
                has_zero = True
        if land_y is None:
            land_y = 0
        if land_y > 0 and has_zero:
            land_y = 0
        return land_y

    def trimmed_shape(self):
        shape = list(filter(lambda a: sum(a) > 0, self.shape))
        sh = []
        for y in range(len(shape)):
            sh.append([])
        for x in range(len(shape[0])):
            s = 0
            for y in range(len(shape)):
                s += shape[y][x]
            if s > 0:
                for y in range(len(shape)):
                    sh[y].append(shape[y][x])
        return sh


    def detect_possible_landing_height(self, trimmed_shape, top):
        top = self.field.top_points()
        bottoms = list(filter(lambda a: a != -1, [*self.bottom_points().values()]))
        base = min(bottoms)
        width = len(bottoms)
        height = len(trimmed_shape)
        result = []
        for x in range(self.field.width + 1 - width):
            h = top[x]
            while self.blocked_at(trimmed_shape, h, x) and h < self.field.height-1:
                h += 1
            y = [(b-base)+h-height+1 for b in bottoms]
            result.append(y)
        return result

    def blocked_at(self, sh, y0, x0):
        for y in range(len(sh)):
                if y0-y < 0:
                    return True
                for x in range(len(sh[0])):
                    if sh[y][x] > 0 and self.field.surface[y0-y][x0+x] > 0:
                        return True
        return False
        


    def blocked(self):
        for y in range(len(self.shape)):
            for x in range(len(self.shape[0])):
                if self.shape[y][x] != 0:
                    if not 0 <= x + self.x <= self.field.width - 1:
                        return True
                    elif self.field.surface[self.y-y][self.x+x] != 0:
                        return True
                    elif self.y - y < 0:
                        return True
        return False

    def move_left(self):
        phantom = self.make_phantom()
        phantom.x -= 1
        if not phantom.blocked():
            self.x = phantom.x

    def move_right(self):
        phantom = self.make_phantom()
        phantom.x += 1
        if not phantom.blocked():
            self.x = phantom.x

    def move_down(self):
        phantom = self.make_phantom()
        phantom.y -= 1
        terminated = False
        if not phantom.blocked():
            self.y = phantom.y
            self.field.distance += 1
            if self.field.distance >= VOLUME_STANDARD['DR'] and self.field.time_drag_st is None:
                self.field.time_drag_st = self.field.time
            if self.field.distance >= self.field.drag_finish and self.field.time_drag is None:
                self.field.time_drag = self.field.time
                if self.field.room.type == 'DR':
                    self.field.end_game()
        else:
            terminated = self.field.land_piece()
        return terminated

    def rotate(self):
        phantom = self.make_phantom()
        if len(phantom.shape) < len(phantom.shape[0]):    # horizontal
            phantom.y += 1
            if phantom.shape[0][0] > 0:
                phantom.x += 1
        elif len(phantom.shape) > len(phantom.shape[0]):  # vertical
            phantom.y -= 1
            if phantom.shape[-1][0] > 0:
                phantom.x -= 1
        super(ActivePiece, phantom).rotate()
        if not phantom.blocked():
            self.x = phantom.x
            self.y = phantom.y
            super(ActivePiece, self).rotate()

    def to_view(self):
        obj = {self.y-y:
               {self.x+x: self.shape[y][x] for x in range(len(self.shape[y])) if self.shape[y][x] > 0}
               for y in range(len(self.shape))}
        obj['pos'] = self.field.pos
        return obj

                # def active_piece_to_view(self):
                #     return {'x': self.active_piece.x,
                #             'y': self.active_piece.y,
                #             'shape': self.active_piece.shape}
