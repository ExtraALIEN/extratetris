from Piece import Piece


class QueuePieces:
    def __init__(self, size=5):
        self.pieces = [Piece() for i in range(size)]
