from django.urls import path

from kernel.views.auth import (
    ChangePassword,
    ResetPassword,
    Lockpick,
)
from kernel.views.home import Home
from kernel.views.who_am_i import WhoAmI

app_name = 'kernel'

urlpatterns = [
    path('', Home.as_view(), name='home'),

    path('who_am_i/', WhoAmI.as_view(), name='who_am_i'),

    path('change_password/', ChangePassword.as_view(), name='change_password'),
    path('reset_password/', ResetPassword.as_view(), name='reset_password'),
    path('lockpick/', Lockpick.as_view(), name='lockpick'),
]
