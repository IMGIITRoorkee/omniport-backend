import swapper
from rest_framework import status, generics, response

from omniport.utils import switcher
from session_auth.models import SessionMap
from session_auth.serializers.login import LoginSerializer
from core.utils.logs import get_logging_function


session_auth_log = get_logging_function('session_auth')

Person = swapper.load_model('kernel', 'Person')

AvatarSerializer = switcher.load_serializer('kernel', 'Person', 'Avatar')


class Login(generics.GenericAPIView):
    """
    This view takes the username and password and if correct, logs the user in
    via cookie-based session authentication
    """

    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        """
        View to serve POST requests
        :param request: the request that is to be responded to
        :param args: arguments
        :param kwargs: keyword arguments
        :return: the response for request
        """

        # Reject authenticated users, right off the gate
        if request.user.is_authenticated:
            response_data = {
                'errors': {
                    'non_field_errors': [
                        'You are already logged in.',
                    ],
                },
            }
            return response.Response(
                data=response_data,
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.user

            # This is a direct replacement for django.contrib.auth.login()
            SessionMap.create_session_map(request=request, user=user)

            session_key = request.session.session_key
            session_auth_log(
                f'Successfully started a session {session_key}',
                'info',
                user
            )

            try:
                user_data = AvatarSerializer(user.person).data
            except Person.DoesNotExist:
                user_data = None
            response_data = {
                'status': 'Successfully logged in',
                'user': user_data,
            }
            return response.Response(
                data=response_data,
                status=status.HTTP_200_OK
            )
        else:
            response_data = {
                'errors': serializer.errors,
            }
            username = serializer.data.get('username')
            session_auth_log(
                'Invalid login attempted on account: '
                f'{username}',
                'warning'
            )
            return response.Response(
                data=response_data,
                status=status.HTTP_400_BAD_REQUEST
            )
