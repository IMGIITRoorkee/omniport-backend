from django.urls import path

from base_auth.views.auth import (
    ChangePassword,
    ResetPassword,
    Lockpick,
)

app_name = 'base_auth'

urlpatterns = [
    path('change_password/', ChangePassword.as_view(), name='change_password'),
    path('reset_password/', ResetPassword.as_view(), name='reset_password'),
    path('lockpick/', Lockpick.as_view(), name='lockpick'),
]
