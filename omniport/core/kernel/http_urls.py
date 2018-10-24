from django.urls import path, include
from rest_framework import routers

from kernel.views.auth import (
    ChangePassword,
    ResetPassword,
    Lockpick,
)
from kernel.views.home import Home
from kernel.views.maintainers import MaintainerViewSet
from kernel.views.rights import Rights
from kernel.views.who_am_i import WhoAmI

app_name = 'kernel'

# DRF routers
router = routers.DefaultRouter()
router.register('maintainers', MaintainerViewSet, base_name='maintainer')

# URL patterns
urlpatterns = [
    path('', Home.as_view(), name='home'),

    path('who_am_i/', WhoAmI.as_view(), name='who_am_i'),

    path('change_password/', ChangePassword.as_view(), name='change_password'),
    path('reset_password/', ResetPassword.as_view(), name='reset_password'),
    path('lockpick/', Lockpick.as_view(), name='lockpick'),

    path('rights/', Rights.as_view(), name='rights'),

    path('', include(router.urls)),
]
