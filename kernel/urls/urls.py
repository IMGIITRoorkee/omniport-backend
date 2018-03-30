from django.urls import path

from kernel.views.home import Home
from kernel.views.who_am_i import WhoAmI

app_name = 'kernel'

urlpatterns = [
    path('', Home.as_view(), name='home'),
    path('who_am_i/', WhoAmI.as_view(), name='who_am_i'),
]
