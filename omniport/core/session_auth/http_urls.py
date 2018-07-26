from django.urls import path

from session_auth.views import (
    Login,
    Logout
)

app_name = 'session_auth'

urlpatterns = [
    path('login/', Login.as_view(), name='login'),
    path('logout/', Logout.as_view(), name='logout'),
]
