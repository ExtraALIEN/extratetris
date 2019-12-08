from ListMethods import buildEmptyFieldList
from QueuePieces import QueuePieces
from ActivePiece import ActivePiece


class Field:

    def __init__(self, room=None, width=12, height=25, ):
        self.room = room
        self.width = width
        self.height = height
        self.surface = buildEmptyFieldList(width, height)
        self.queue = QueuePieces()

    def top_points(self):
        def top_point(x):
            for y in range(self.height):
                if self.surface[y][x] > 0:
                    return y
            return 0
        return [top_point(x) for x in range(self.width)]

    def create_piece(self):
        piece = self.queue.release_next_piece()
        piece = ActivePiece(piece,
                            field=self,
                            field_surface=self.top_points(),
                            x=self.width//2,
                            y=self.height)
        piece.dev_show()
        return piece
