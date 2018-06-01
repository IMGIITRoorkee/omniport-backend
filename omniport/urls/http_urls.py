from django.urls import path, include
from django.views.generic import TemplateView

from kernel.admin.site import omnipotence
from omniport.views.csrf import EnsureCsrf

http_urlpatterns = [
    # The root path should serve the React app and assets from NGINX itself
    path('', TemplateView.as_view(template_name='404.html'), name='home'),

    # Ensures a CSRF cookie on the client
    path('ensure_csrf/', EnsureCsrf.as_view(), name='ensure_csrf'),

    # Django admin URL dispatcher
    path('omnipotence/', omnipotence.urls),

    # Django REST Framework URL dispatcher
    path('rest/', include('rest_framework.urls')),
]
