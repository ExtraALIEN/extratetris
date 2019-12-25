from engine.Piece import Piece


class QueuePieces:
    def __init__(self, size=5):
        self.pieces = [Piece() for i in range(size)]

    def release_next_piece(self):
        next_piece = self.pieces.pop(0)
        self.pieces.append(Piece())
        return next_piece

    def to_view(self):
        return {i:
                {y:
                 {x: self.pieces[i].shape[y][x] for x in range(len(self.pieces[i].shape[y]))}
                 for y in range(len(self.pieces[i].shape))}
                for i in range(len(self.pieces))}
