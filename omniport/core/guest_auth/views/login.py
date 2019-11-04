import swapper
from rest_framework import status, generics, response
from django.contrib.auth import login
from django.conf import settings

from omniport.utils import switcher
from base_auth.managers.get_user import get_user
from session_auth.models import SessionMap

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

        guest_user = get_user(GUEST_USERNAME)
        request.user = guest_user
        # This is a direct replacement for django.contrib.auth.login()

        login(request, guest_user, backend='base_auth.backends.generalised.GeneralisedAuthBackend')

        SessionMap.create_session_map(request=request, user=guest_user, new=False)

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
