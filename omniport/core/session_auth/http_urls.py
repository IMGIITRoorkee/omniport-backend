from django.urls import path

from session_auth.views.login import Login
from session_auth.views.logout import Logout

app_name = 'session_auth'

urlpatterns = [
    path('login/', Login.as_view(), name='login'),
    path('logout/', Logout.as_view(), name='logout'),
]
