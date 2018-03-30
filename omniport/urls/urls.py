from omniport.urls.base import *
from omniport.utils import get_app_urlpatterns, get_service_urlpatterns

urlpatterns += get_service_urlpatterns()
urlpatterns += get_app_urlpatterns()
