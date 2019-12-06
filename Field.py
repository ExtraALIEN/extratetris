from ListMethods import build_empty_field_list
from QueuePieces import Queue_pieces


class Field:
    def __init__(self, width=12, height=25):
        self.width = width
        self.height = height
        self.surface = build_empty_field_list(width, height)
        self.queue = Queue_pieces()

    def top_point(self, x):
        for y in range(self.height):
            if self.surface[y][x] > 0:
                return y
        return 0

    def top_points(self):
        return [self.top_point(x) for x in range(self.width)]
