from random import randint
from engine.ListMethods import rotate as list_rotate

SHAPES = [
    [[1, 1, 1, 1]],
    [[1, 1, 1], [0, 1, 0]],
    [[1, 1, 0], [0, 1, 1]],
    [[0, 1, 1], [1, 1, 0]],
    [[1, 1], [1, 1]],
    [[1, 1, 1], [1, 0, 0]],
    [[1, 1, 1], [0, 0, 1]]
]


def get_shape(number):
    return SHAPES[number]


class Piece:
    def __init__(self):
        self.shape = get_shape(randint(0, len(SHAPES)-1))
        for i in range(randint(0, 4)):
            self.rotate()

    def rotate(self, clockwise=True):
        self.shape = list_rotate(self.shape, clockwise)
