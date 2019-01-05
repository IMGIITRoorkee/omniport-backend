from django.urls import path
from oauth2_provider.views import (
    AuthorizationView,
    TokenView,
    RevokeTokenView,
)

app_name = 'open_auth'

urlpatterns = [
    path('authorize/', AuthorizationView.as_view(), name='authorize'),
    path('token/', TokenView.as_view(), name='token'),
    path('revoke_token/', RevokeTokenView.as_view(), name='revoke_token'),
]
