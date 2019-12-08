from ListMethods import buildEmptyFieldList
from QueuePieces import QueuePieces
from ActivePiece import ActivePiece


class Field:
    _counter = 0

    def __init__(self, room_id, width=12, height=25, ):
        self.width = width
        self.height = height
        self.surface = buildEmptyFieldList(width, height)
        self.queue = QueuePieces()
        self.room_id = room_id
        self.id = Field._counter
        Field._counter += 1

    def top_point(self, x):
        for y in range(self.height):
            if self.surface[y][x] > 0:
                return y
        return 0

    def top_points(self):
        return [self.top_point(x) for x in range(self.width)]

    def create_piece(self):
        piece = self.queue.release_next_piece()
        piece = ActivePiece(piece, field_surface=self.top_points(), x=self.width//2, y=self.height)
        piece.dev_show()
        return piece
