from omniport.urls.http_urls import http_urlpatterns
from omniport.urls.ws_urls import ws_urlpatterns
from omniport.utils.urls import get_urlpatterns

http_urlpatterns += get_urlpatterns('core', 'http')
http_urlpatterns += get_urlpatterns('services', 'http')
http_urlpatterns += get_urlpatterns('apps', 'http')

ws_urlpatterns += get_urlpatterns('core', 'ws')
ws_urlpatterns += get_urlpatterns('services', 'ws')
ws_urlpatterns += get_urlpatterns('apps', 'ws')
