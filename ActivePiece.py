from Piece import Piece


class ActivePiece(Piece):
    def __init__(self, current_piece, x, y):
        self.shape = current_piece.shape
        self.x = x
        self.y = y


    def dev_show(self):
        print(self.shape)
        print(self.x)
        print(self.y)
