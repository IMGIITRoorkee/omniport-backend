from django.urls import path

from protocol_tests.consumers import PingPong

urlpatterns = [
    # WebSocket Ping Pong!
    path('ping_pong/', PingPong, name='ping_pong'),
]
