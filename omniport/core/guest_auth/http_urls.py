from django.urls import path

from guest_auth.views.login import Login
from guest_auth.views.logout import Logout

app_name = 'guest_auth'

urlpatterns = [
    path('login/', Login.as_view(), name='login'),
    path('logout/', Logout.as_view(), name='logout'),
]
