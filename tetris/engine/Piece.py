from random import randint, random
from engine.ListMethods import rotate as list_rotate, sum
from web.helpers import SHAPES, POWERUPS

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

    def build_powerup(self, powerup_chance):
        num = random()
        if num < powerup_chance:
            x = randint(0, len(POWERUPS)-1)
            powerup_code = (x+1)*100
            left = randint(0, sum(self.shape)-1)
            for y in range(len(self.shape)):
                for x in range(len(self.shape[y])):
                    if self.shape[y][x] > 0:
                        if left == 0:
                            self.shape[y][x] += powerup_code
                            return
                        left -= 1
