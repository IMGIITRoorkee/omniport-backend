from django.urls import path, include

from kernel.admin.site import omnipotence
from omniport.views.csrf import EnsureCsrf
from omniport.views.hello_world import HelloWorld
from omniport.views.ping_pong import PingPong

http_urlpatterns = [
    # TODO
    # Home
    # The root path should serve the React app and assets from NGINX itself
    path('', HelloWorld.as_view(), name='home'),

    # Hello World!
    path('hello_world/', HelloWorld.as_view(), name='hello_world'),

    # WebSocket Ping Pong!
    path('ping_pong/', PingPong.as_view(), name='ping_pong'),

    # Ensures a CSRF cookie on the client
    path('ensure_csrf/', EnsureCsrf.as_view(), name='ensure_csrf'),

    # Django admin URL dispatcher
    path('omnipotence/', omnipotence.urls),

    # Django REST Framework URL dispatcher
    path('rest/', include('rest_framework.urls')),
]
