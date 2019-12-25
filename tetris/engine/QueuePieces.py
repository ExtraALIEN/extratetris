from engine.Piece import Piece


class QueuePieces:
    def __init__(self, size=5):
        self.pieces = [Piece() for i in range(size)]

    def release_next_piece(self):
        next_piece = self.pieces.pop(0)
        self.pieces.append(Piece())
        return next_piece

    def to_view(self):
        return {x: self.pieces[x].shape for x in range(len(self.pieces))}
