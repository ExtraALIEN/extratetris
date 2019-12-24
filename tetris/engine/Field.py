from engine.ListMethods import buildEmptyFieldList
from engine.QueuePieces import QueuePieces
from engine.ActivePiece import ActivePiece


class Field:

    def __init__(self, room=None, width=12, height=25, ):
        self.room = room
        self.width = width
        self.height = height
        self.surface = buildEmptyFieldList(width, height)
        self.queue = QueuePieces()
        self.active_piece = self.create_piece()
        self.websocket = None
        self.player = None

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
                            x=self.width//2 - 1,
                            y=self.height-1)
        piece.dev_show()
        return piece

    def land_piece(self):
        for y in range(len(self.active_piece.shape)):
            for x in range(len(self.active_piece.shape[0])):
                if self.active_piece.shape[y][x] > 0:
                    self.surface[self.active_piece.y-y][x+self.active_piece.x] \
                        = self.active_piece.shape[y][x]
        self.active_piece = self.create_piece()

    def queue_to_view(self):
        return {x: self.queue.pieces[x].shape for x in range(len(self.queue.pieces))}

    def active_piece_to_view(self):
        return {'x': self.active_piece.x,
                'y': self.active_piece.y,
                'shape': self.active_piece.shape}
