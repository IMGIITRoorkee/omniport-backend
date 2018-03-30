"""omniport URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
"""

from django.urls import path, include

from kernel.admin.site import omnipotence
from omniport.views.hello_world import HelloWorld

urlpatterns = [
    # Hello World!
    path('', HelloWorld.as_view(), name='hello_world'),

    # Django admin URL dispatcher
    path('omnipotence/', omnipotence.urls),

    # Django REST Framework URL dispatcher
    path('rest/', include('rest_framework.urls')),

    # Kernel URL dispatcher
    path('kernel/', include('kernel.urls')),
]
