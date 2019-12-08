from Piece import Piece


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


    def move_left(self):
        if self.x > 0:
            self.x -= 1

    def move_right(self):
        if self.x < self.field.width - len(self.shape[0]):
            self.x += 1

    def rotate(self):
        def blocked(self):
            radius = len(self.shape) // 2
            if self.x < radius and self.shape[-1][0] > 0:
                return True
            elif (self.field.width - 1) - self.x < radius and self.shape[0][-1] > 0:
                return True
            return False

        if not blocked(self):
            if len(self.shape) > len(self.shape[0]):
                self.y += 1
            elif len(self.shape) < len(self.shape[0]):
                self.y -= 1
            super(ActivePiece, self).rotate()
        else:
            print('blocked', self.x)
