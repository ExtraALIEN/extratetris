import asyncio
import json
from channels.generic.websocket import JsonWebsocketConsumer
from ws.roomUtils import make_connect

class Connector(JsonWebsocketConsumer):
    def connect(self):
        self.accept()

    def receive_json(self, data):
        print(data)
        type = data['type']
        if type == 'connect':
            make_connect(self, data)
            self.send_json(json.dumps({'type': 2}))
        else:
            self.send_json({'type':3})


    def disconnect(self, close_code):
        pass
