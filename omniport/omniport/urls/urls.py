from django.conf.urls.static import static

from omniport.urls.http_urls import http_urlpatterns
from omniport.urls.ws_urls import ws_urlpatterns
from django.conf import settings

settings.DISCOVERY.prepare_urlpatterns()

http_urlpatterns += settings.DISCOVERY.service_http_urlpatterns
http_urlpatterns += settings.DISCOVERY.app_http_urlpatterns

ws_urlpatterns += settings.DISCOVERY.service_ws_urlpatterns
ws_urlpatterns += settings.DISCOVERY.app_ws_urlpatterns

if settings.DEBUG:
    http_urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )
    http_urlpatterns += static(
        settings.BRANDING_URL,
        document_root=settings.BRANDING_ROOT
    )
