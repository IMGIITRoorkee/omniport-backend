from django.urls import path

from token_auth.views import (
    ObtainPair,
    Refresh,
    Verify,
)

app_name = 'token_auth'

urlpatterns = [
    path('obtain_pair/', ObtainPair.as_view(), name='obtain_pair'),
    path('refresh/', Refresh.as_view(), name='refresh'),
    path('verify/', Verify.as_view(), name='verify'),
]
