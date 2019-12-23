import swapper
from rest_framework import status, generics, response
from django.contrib.auth import login
from django.conf import settings

from omniport.utils import switcher
from base_auth.models import User
from base_auth.managers.get_user import get_user
from session_auth.models import SessionMap

from guest_auth.utils.create_guest import create_guest

Person = swapper.load_model('kernel', 'Person')

AvatarSerializer = switcher.load_serializer('kernel', 'Person', 'Avatar')

GUEST_USERNAME = settings.GUEST_USERNAME


class Login(generics.GenericAPIView):
    """
    This view takes the username and password and if correct, logs the user in
    via cookie-based session authentication
    """

    def get(self, request, *args, **kwargs):
        """
        View to serve POST requests
        :param request: the request that is to be responded to
        :param args: arguments
        :param kwargs: keyword arguments
        :return: the response for request
        """
        try:
            guest_user = get_user(GUEST_USERNAME)
        except User.DoesNotExist:
            guest_user = create_guest()
        # This is a direct replacement for django.contrib.auth.login()

        login(
            request=request,
            user=guest_user,
            backend='base_auth.backends.generalised.GeneralisedAuthBackend'
        )

        SessionMap.create_session_map(
            request=request,
            user=guest_user,
            new=False
        )

        try:
            user_data = AvatarSerializer(guest_user.person).data
        except Person.DoesNotExist:
            user_data = None
        response_data = {
            'status': 'Successfully logged in.',
            'user': user_data,
        }
        return response.Response(
            data=response_data,
            status=status.HTTP_200_OK
        )
