import asyncio
import json
from channels.generic.websocket import JsonWebsocketConsumer
from engine.roomUtils import make_connect, create_room, find_next_id

class Connector(JsonWebsocketConsumer):
    def connect(self):
        self.accept()

    def receive_json(self, data):
        print(data)
        self.send_json(2)
        type = data['type']
        if type == 'connect':
            print(type)
            self.send_json(make_connect(self, data))
        else:
            self.send_json({'type': 3})


    def disconnect(self, close_code):
        pass


class CreateRoom(JsonWebsocketConsumer):
    def connect(self):
        self.accept()
        self.send_json('connected')

    def receive_json(self, data):
        if data['command'] == 'init_room':
            create_room(find_next_id(), int(data['players']))


    def disconnect(self, close_code):
        pass