from django.urls import path, include
from oauth2_provider.views import (
    AuthorizationView,
    TokenView,
    RevokeTokenView,
)
from rest_framework import routers
from rest_framework.authentication import SessionAuthentication

from open_auth.views.application import ApplicationViewSet
from open_auth.views.retrieve_data import GetUserData
from open_auth.views.throttling import ThrottledOAuthLibView

router = routers.SimpleRouter()
router.register('application', ApplicationViewSet, basename='application')

app_name = 'open_auth'

urlpatterns = [
    path(
        'authorise/',
        ThrottledOAuthLibView.as_view(
            oauthlib_view=AuthorizationView.as_view(),
            # DRF replaces request.user with the anonymous user when no
            # authenticator matches, and the consent screen needs the session
            authentication_classes=[SessionAuthentication],
        ),
        name='authorise'
    ),
    path(
        'token/',
        ThrottledOAuthLibView.as_view(
            oauthlib_view=TokenView.as_view(),
        ),
        name='token'
    ),
    path(
        'revoke_token/',
        ThrottledOAuthLibView.as_view(
            oauthlib_view=RevokeTokenView.as_view(),
        ),
        name='revoke_token'
    ),
    path(
        'get_user_data/',
        GetUserData.as_view(),
        name='get_user_data'
    ),
    path('', include(router.urls)),
]
