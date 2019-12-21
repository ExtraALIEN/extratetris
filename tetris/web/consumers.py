import asyncio
import json
from channels.generic.websocket import JsonWebsocketConsumer
from engine.roomUtils import make_connect, create_room, find_next_id, init_room, room_disconnect

class ConnectRoom(JsonWebsocketConsumer):
    def connect(self):
        self.accept()


    def receive_json(self, data):
        print(data)
        type = data['type']
        if type == 'init':
            init_room(self, data)
        elif type == 'connect':
            make_connect(self, data)
        elif type == 'disconnect':
            room_disconnect(self, data)



    def disconnect(self, close_code):
        room_disconnect(self, False)



class CreateRoom(JsonWebsocketConsumer):
    def connect(self):
        self.accept()
        self.send_json('connected')

    def receive_json(self, data):
        if data['command'] == 'init_room':
            create_room(find_next_id(), int(data['players']))


    def disconnect(self, close_code):
        pass
