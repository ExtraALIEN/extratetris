from ListMethods import buildEmptyFieldList
from QueuePieces import QueuePieces


class Field:
    def __init__(self, width=12, height=25):
        self.width = width
        self.height = height
        self.surface = buildEmptyFieldList(width, height)
        self.queue = QueuePieces()

    def topPoint(self, x):
        for y in range(self.height):
            if self.surface[y][x] > 0:
                return y
        return 0

    def topPoints(self):
        return [self.topPoint(x) for x in range(self.width)]
