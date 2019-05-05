from django.urls import path, include

from omniport.admin.site import omnipotence

http_urlpatterns = [
    # Django admin URL dispatcher
    path('omnipotence/', omnipotence.urls),

    # PyPI packages URL dispatcher
    path('tinymce/', include('tinymce.urls')),

    # The almighty swappable kernel
    path('kernel/', include('kernel.http_urls')),

    # Authentication
    path('base_auth/', include('base_auth.http_urls')),
    path('session_auth/', include('session_auth.http_urls')),
    path('token_auth/', include('token_auth.http_urls')),
    path('open_auth/', include('open_auth.http_urls')),

    # Bootstrapping
    path('bootstrap/', include('bootstrap.http_urls')),
]

http_urlpatterns_fallthrough = [
    # Formula 1
    path('', include('formula_one.http_urls')),
]
