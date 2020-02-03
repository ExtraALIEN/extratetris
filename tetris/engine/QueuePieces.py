from engine.Piece import Piece


class QueuePieces:
    def __init__(self, pos, size=5):
        self.pos = pos
        self.pieces = [Piece() for i in range(size)]
        self.chance = 0

    def release_next_piece(self, powerup_chance=0.02):
        next_piece = self.pieces.pop(0)
        self.pieces.append(Piece())
        if powerup_chance > 0:
            next_piece.build_powerup(powerup_chance)
            self.chance += powerup_chance
            print(self.chance)
        return next_piece

    def to_view(self):
        obj = {i:
                {y:
                 {x: self.pieces[i].shape[y][x] for x in range(len(self.pieces[i].shape[y]))}
                 for y in range(len(self.pieces[i].shape))}
                for i in range(len(self.pieces))}
        obj['pos'] = self.pos
        return obj
