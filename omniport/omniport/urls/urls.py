from django.conf.urls.static import static

from omniport.urls.http_urls import http_urlpatterns
from omniport.urls.ws_urls import ws_urlpatterns
from omniport.utils.urls import get_urlpatterns
from django.conf import settings

http_urlpatterns += get_urlpatterns('core', 'http')
http_urlpatterns += get_urlpatterns('services', 'http')
http_urlpatterns += get_urlpatterns('apps', 'http')

ws_urlpatterns += get_urlpatterns('core', 'ws')
ws_urlpatterns += get_urlpatterns('services', 'ws')
ws_urlpatterns += get_urlpatterns('apps', 'ws')

if settings.DEBUG:
    http_urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )
    http_urlpatterns += static(
        settings.BRANDING_URL,
        document_root=settings.BRANDING_ROOT
    )
