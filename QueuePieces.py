from Piece import Piece


class Queue_pieces:
    def __init__(self, size=5):
        self.pieces = [Piece() for i in range(size)]

    def release_next_piece(self):
        next_piece = self.pieces.pop(0)
        self.pieces.append(Piece())
        return next_piece
