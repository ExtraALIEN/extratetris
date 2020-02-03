from random import randint
from engine.ListMethods import rotate as list_rotate

SHAPES = [
    [[1, 1, 1, 1]],
    [[1, 1, 1], [0, 1, 0], [0, 0, 0]],
    [[1, 1, 0], [0, 1, 1]],
    [[0, 1, 1], [1, 1, 0]],
    [[1, 1], [1, 1]],
    [[1, 1, 1], [1, 0, 0], [0, 0, 0]],
    [[1, 1, 1], [0, 0, 1], [0, 0, 0]]
]

chance = 0
def add_chance(ch):
    chance += ch
    print(chance)

def get_shape(number, color):
    sh = []
    for y in SHAPES[number]:
        new_y = []
        for x in y:
            if x == 1:
                new_y.append(color)
            else:
                new_y.append(0)
        sh.append(new_y)
    return sh


class Piece:
    def __init__(self):
        self.color = randint(1, 8)
        self.shape = get_shape(randint(0, len(SHAPES)-1), self.color)
        for i in range(randint(0, 4)):
            self.rotate()


    def rotate(self, clockwise=True):
        self.shape = list_rotate(self.shape, clockwise)

    def build_powerup(self, powerup_chance=0.02):
        pass
