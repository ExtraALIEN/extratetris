from django.urls import path
from channels.routing import ProtocolTypeRouter, URLRouter

from web.consumers import WsConsumer
application = ProtocolTypeRouter({
    'websocket':
            URLRouter(
                [
                    path('ws/', WsConsumer),
                ]
            )
    })
