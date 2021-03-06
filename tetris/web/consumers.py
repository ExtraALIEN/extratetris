import asyncio
import json
from channels.generic.websocket import JsonWebsocketConsumer
from engine.roomUtils import room_connect, create_room, find_next_id, \
        init_room, room_hard_disconnect, room_disconnect, add_bot, del_bot
from engine.ingame import add_ready, process_command
from engine.lobbyUtils import connect_lobby, disconnect_lobby


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
        elif type == 'add-bot':
            add_bot(data)
        elif type == 'del-bot':
            del_bot(data)

    def disconnect(self, close_code):
        room_hard_disconnect(self)


class CreateRoom(JsonWebsocketConsumer):
    def connect(self):
        self.accept()
        self.send_json('connected')

    def receive_json(self, data):
        if data['command'] == 'init_room':
            create_room(find_next_id(), int(data['players']),
                        data['game_type'], float(data['volume']),
                        bool(data['ranked']), bool(data['crazy']))

    def disconnect(self, close_code):
        pass


class Lobby(JsonWebsocketConsumer):
    def connect(self):
        self.accept()
        connect_lobby(self)

    def disconnect(self, close_code):
        disconnect_lobby(self)
        pass
