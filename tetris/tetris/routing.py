from django.urls import path
from channels.routing import ProtocolTypeRouter, URLRouter

from web.consumers import Connector, CreateRoom
application = ProtocolTypeRouter({
    'websocket':
            URLRouter(
                [
                    path('ws/connect/', Connector),
                    path('ws/create/', CreateRoom),
                ]
            )
    })
