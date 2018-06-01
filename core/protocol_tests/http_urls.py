from django.urls import path

from protocol_tests.views import HelloWorld, PingPong

app_name = 'protocol_tests'

urlpatterns = [
    path('hello_world/', HelloWorld.as_view(), name='hello_world'),
    path('ping_pong/', PingPong.as_view(), name='ping_pong'),
]
