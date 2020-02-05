from engine.Piece import Piece
from random import randint
from web.helpers import SHAPES

class QueuePieces:
    def __init__(self, pos, size=5):
        self.pos = pos
        self.size = size
        self.pieces = [Piece(color=randint(1, 8), shape_number=randint(0, len(SHAPES)-1)) for i in range(self.size)]


    def release_next_piece(self, powerup_chance=0.02):
        next_piece = self.pieces.pop(0)
        self.pieces.append(Piece(color=randint(1, 8), shape_number=randint(0, len(SHAPES)-1)))
        if powerup_chance > 0:
            next_piece.build_powerup(powerup_chance)
        return next_piece

    def to_view(self):
        obj = {i:
                {y:
                 {x: self.pieces[i].shape[y][x] for x in range(len(self.pieces[i].shape[y]))}
                 for y in range(len(self.pieces[i].shape))}
                for i in range(len(self.pieces))}
        obj['pos'] = self.pos
        return obj

    def fill(self, color, shape_number):
        self.pieces = [Piece(color=color, shape_number=shape_number) for i in range(self.size)]
