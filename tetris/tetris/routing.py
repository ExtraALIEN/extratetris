from django.urls import path
from channels.routing import ProtocolTypeRouter, URLRouter

from web.consumers import ConnectRoom, CreateRoom
application = ProtocolTypeRouter({
    'websocket':
            URLRouter(
                [
                    path('ws/connect/', ConnectRoom),
                    path('ws/create/', CreateRoom),
                ]
            )
    })
