from omniport.urls.http_urls import http_urlpatterns
from omniport.urls.ws_urls import ws_urlpatterns
from omniport.utils import (
    get_core_urlpatterns,
    get_app_urlpatterns,
    get_service_urlpatterns,
)

http_urlpatterns += get_core_urlpatterns(protocol='http')
http_urlpatterns += get_service_urlpatterns(protocol='http')
http_urlpatterns += get_app_urlpatterns(protocol='http')

ws_urlpatterns += get_core_urlpatterns(protocol='ws')
ws_urlpatterns += get_service_urlpatterns(protocol='ws')
ws_urlpatterns += get_app_urlpatterns(protocol='ws')
