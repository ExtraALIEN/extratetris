class Bot:
    def __init__(self, room, pos):
        self.username = '* bot *'
        self.room = room
        self.pos = pos
        self.field = room.fields[pos]
