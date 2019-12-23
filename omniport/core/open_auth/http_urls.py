from django.urls import path, include
from django.views.decorators.http import require_POST
from oauth2_provider.views import (
    AuthorizationView,
    TokenView,
    RevokeTokenView,
)
from rest_framework import routers

from open_auth.views.application import ApplicationViewSet
from open_auth.views.retrieve_data import GetUserData

router = routers.SimpleRouter()
router.register('application', ApplicationViewSet, base_name='application')

app_name = 'open_auth'

urlpatterns = [
    path(
        'authorise/',
        require_POST(AuthorizationView.as_view()),
        name='authorise'
    ),
    path(
        'token/',
        TokenView.as_view(),
        name='token'
    ),
    path(
        'revoke_token/',
        RevokeTokenView.as_view(),
        name='revoke_token'
    ),

    path('', include(router.urls)),
    path('get_user_data/', GetUserData.as_view(), name='get_user_data'),
]
