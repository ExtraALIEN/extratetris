from Piece import Piece


class ActivePiece(Piece):
    def __init__(self, current_piece, x, y, field_surface):
        self.shape = current_piece.shape
        self.x = x
        self.y = y
        self.field_surface = field_surface


    def dev_show(self):
        print(self.shape)
        print(self.field_surface)
        print(self.x)
        print(self.y)

    def bottom_point(self, x):
        bottom = 0
        for y in range(len(self.shape)-1, -1,-1):
            if self.shape[y][x] != 0:
                return self.y-y
        return self.y

    def bottom_points(self):
        return [self.bottom_point(x) for x in range(len(self.shape[0]))]
