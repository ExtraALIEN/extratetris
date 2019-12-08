from Field import Field


class Room:
    def __init__(self, size):
        self.fields = [Field(room=self) for i in range(size)]
