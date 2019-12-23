from django.urls import path

from session_auth.views.login import Login
from session_auth.views.logout import Logout
from session_auth.views.illustration_roulette import IllustrationRoulette

app_name = 'session_auth'

urlpatterns = [
    path('login/', Login.as_view(), name='login'),
    path('logout/', Logout.as_view(), name='logout'),
    path(
        'illustration_roulette/',
        IllustrationRoulette.as_view(),
        name='illustration_roulette'
    )
]
