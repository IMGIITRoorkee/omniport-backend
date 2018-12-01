from django.urls import path, include
from rest_framework import routers

from kernel.views.maintainers import MaintainerViewSet
from kernel.views.rights import Rights
from kernel.views.who_am_i import WhoAmI

app_name = 'kernel'

# DRF routers
router = routers.SimpleRouter()
router.register('maintainers', MaintainerViewSet, base_name='maintainer')

# URL patterns
urlpatterns = [
    path('who_am_i/', WhoAmI.as_view(), name='who_am_i'),
    path('rights/', Rights.as_view(), name='rights'),

    path('', include(router.urls)),
]
