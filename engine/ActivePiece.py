from Piece import Piece
import copy

class ActivePiece(Piece):
    def __init__(self, current_piece, x, y, field, field_surface):
        self.shape = current_piece.shape
        self.x = x
        self.prev_x = x
        self.y = y
        self.field = field
        self.field_surface = field_surface


    def dev_show(self):
        print(self.shape)
        print(self.field_surface)
        print(self.x)
        print(self.y)

    def bottom_points(self):
        def bottom_point(x):
            for y in range(len(self.shape)-1, -1, -1):
                if self.shape[y][x] != 0:
                    return self.y-y
            return self.y
        return [bottom_point(x) for x in range(len(self.shape[0]))]

    def blocked(self):
        for y in range(len(self.shape)):
            for x in range(len(self.shape[0])):
                if self.shape[y][x] != 0:
                    if not 0 <= x + self.x <= self.field.width - 1:
                        return True
                    if self.field.surface[y][x] != 0:
                        return True
        return False

    def move_left(self):
        phantom = copy.deepcopy(self)
        phantom.x -= 1
        if not phantom.blocked():
            self.x = phantom.x

    def move_right(self):
        phantom = copy.deepcopy(self)
        phantom.x += 1
        if not phantom.blocked():
            self.x = phantom.x

    def move_down(self):
        phantom = copy.deepcopy(self)
        phantom.y -= 1
        if not phantom.blocked():
            self.y = phantom.y
            self.check_landing()

    def check_landing(self):
        pass

    def rotate(self):
        phantom = copy.deepcopy(self)
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
