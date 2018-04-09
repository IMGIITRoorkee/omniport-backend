from django.urls import path

from omniport.consumers.ping_pong import PingPong

ws_urlpatterns = [
    # WebSocket Ping Pong!
    path('', PingPong, name='ping_pong'),
]
