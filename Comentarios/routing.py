from channels.routing import ProtocolTypeRouter, URLRouter
from django.urls import path

from app.consumers import *

application = ProtocolTypeRouter({
    "websocket": URLRouter([
        path("ws/",RealTime, name='websocket'),
    ])
})