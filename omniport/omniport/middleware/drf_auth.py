from django.contrib.auth import get_user
from django.contrib.auth.models import AnonymousUser
from django.utils.functional import SimpleLazyObject
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.request import Request
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from sentry_sdk import configure_scope

from omniport.settings.configuration.base import CONFIGURATION as _CONF


def get_user_jwt(request):
    """
    Process the request to find the user associated with the request
    :param request: the request which is to be authenticated
    :return: the user instance if authenticated, AnonymousUser() otherwise
    """

    user = get_user(request)

    if user.is_authenticated:
        return user

    try:
        user_jwt, _ = JWTAuthentication().authenticate(Request(request))
        if user_jwt is not None:
            return user_jwt
    except (AuthenticationFailed, InvalidToken, TokenError, TypeError):
        # There may be other exceptions but these are the only ones I could see
        pass

    return user or AnonymousUser()


class DrfAuth:
    """
    Make the user available to middleware, which is not otherwise possible in
    the Django REST framework architecture
    """

    def __init__(self, get_response):
        """
        Write the __init__ function exactly as the Django documentations says
        """

        self.get_response = get_response

    def __call__(self, request):
        """
        Perform the actual processing on the request before it goes to the view
        and on the response returned by the view
        :param request: the request being processed
        :return: the processed response
        """

        request.user = SimpleLazyObject(lambda: get_user_jwt(request))

        # Provide the user context to any exception raised by sentry
        if 'sentry' in _CONF.integrations:
            with configure_scope() as scope:
                if request.user:
                    scope.user = {'username': request.user.username}

        response = self.get_response(request)

        return response
