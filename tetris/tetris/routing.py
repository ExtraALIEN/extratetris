from django.conf.urls import url
from channels.routing import ProtocolTypeRouter, URLRouter

from web.consumers import WsConsumer
application = ProtocolTypeRouter({
    'websocket':
            URLRouter(
                [
                    url("test/", WsConsumer),
                ]
            )
    })
