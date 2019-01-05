from django.urls import path

from kernel.views.rights import Rights
from kernel.views.who_am_i import WhoAmI

app_name = 'kernel'

# URL patterns
urlpatterns = [
    path('who_am_i/', WhoAmI.as_view(), name='who_am_i'),
    path('rights/', Rights.as_view(), name='rights'),
]
