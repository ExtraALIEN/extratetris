from engine.Piece import Piece

class ActivePiece(Piece):
    def __init__(self, current_piece, x, y, field):
        self.shape = current_piece.shape
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
            for y in range(len(self.shape)-1, -1, -1):
                if self.shape[y][x] != 0:
                    return self.y-y
            return self.y
        return {x+self.x: bottom_point(x) for x in range(len(self.shape[0]))}

    def detect_landing_row(self):
        land_y = None
        points = self.bottom_points()
        for x in points:
            y = points[x]
            if y > 0:
                if self.field.surface[y-1][x] > 0:
                    if land_y is None:
                        land_y = y
                    elif y-1 < land_y:
                        land_y = y
            elif y == 0:
                return 0
        print(land_y, points)
        return land_y

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
        return {self.y-y:
                {self.x+x: self.shape[y][x] for x in range(len(self.shape[y]))}
                for y in range(len(self.shape))}
