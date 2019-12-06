SHAPES = [
    [[1,1,1,1]],
    [[1,1,1],[0,1,0]],
    [[1,1,0],[0,1,1]],
    [[0,1,1],[1,1,0]],
    [[1,1],[1,1]],
    [[1,1,1],[1,0,0]],
    [[1,1,1],[0,0,1]]
]

from random import randint
from ListMethods import rotate as list_rotate

def getShape(number):
    return SHAPES[number]


class Piece:
    def __init__(self):
        self.shape = getShape(randint(0,6))

    def rotate(self, clockwise=True):
        self.shape = list_rotate(self.shape, clockwise)
