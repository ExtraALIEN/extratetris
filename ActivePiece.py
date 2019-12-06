from Piece import Piece


class ActivePiece(Piece):
    def __init__(self, current_piece):
        self.shape = current_piece.shape
