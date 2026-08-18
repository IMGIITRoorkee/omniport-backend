"""
Since the SimpleJWT project is incompatible with the JSON API plugin for the
Django REST framework, we override the views to explicitly use the parsers and
renderers as they were before JSON API came along.
"""

from django.conf import settings

from rest_framework.parsers import (
    JSONParser,
    FormParser,
    MultiPartParser,
)
from rest_framework.renderers import (
    JSONRenderer,
    BrowsableAPIRenderer,
)
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

PARSERS_MINUS_JSON_API = (JSONParser, FormParser, MultiPartParser,)
RENDERERS_MINUS_JSON_API = (
    (JSONRenderer, BrowsableAPIRenderer,) if settings.DEBUG else (JSONRenderer,)
)


class ObtainPair(TokenObtainPairView):
    """
    Remove the effect of the addition of project-wide JSON API from the view
    """

    throttle_scope = 'login'
    parser_classes = PARSERS_MINUS_JSON_API
    renderer_classes = RENDERERS_MINUS_JSON_API


class Refresh(TokenRefreshView):
    """
    Remove the effect of the addition of project-wide JSON API from the view
    """

    parser_classes = PARSERS_MINUS_JSON_API
    renderer_classes = RENDERERS_MINUS_JSON_API


class Verify(TokenVerifyView):
    """
    Remove the effect of the addition of project-wide JSON API from the view
    """

    parser_classes = PARSERS_MINUS_JSON_API
    renderer_classes = RENDERERS_MINUS_JSON_API
