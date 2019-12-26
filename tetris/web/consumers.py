import asyncio
import json
from channels.generic.websocket import JsonWebsocketConsumer
from engine.roomUtils import room_connect, create_room, find_next_id, \
        init_room, room_hard_disconnect, room_disconnect
from engine.ingame import add_ready, process_command

class ConnectRoom(JsonWebsocketConsumer):
    def connect(self):
        self.accept()


    def receive_json(self, data):
        type = data['type']
        if type == 'init':
            init_room(self, data)
        elif type == 'connect':
            room_connect(self, data)
        elif type == 'disconnect':
            room_disconnect(self, data)
        elif type == 'ready':
            add_ready(self)
        elif type == 'control':
            process_command(self, data)



    def disconnect(self, close_code):
        room_hard_disconnect(self)



class CreateRoom(JsonWebsocketConsumer):
    def connect(self):
        self.accept()
        self.send_json('connected')

    def receive_json(self, data):
        if data['command'] == 'init_room':
            create_room(find_next_id(), int(data['players']))


    def disconnect(self, close_code):
        pass
