from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from django.urls import path

from omniport.urls import ws_urlpatterns

ws_urlpatterns = [
    path('ws/', URLRouter(ws_urlpatterns)),
]

application = ProtocolTypeRouter({
    # http -> Django views is added by default
    'websocket': AuthMiddlewareStack(
        URLRouter(ws_urlpatterns)
    ),
})
