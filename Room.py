from Field import Field


class Room:
    _counter = 0
    
    def __init__(self, size):
        self.id = Room._counter
        Room._counter += 1
        self.fields = [Field(room_id=self.id) for i in range(size)]
