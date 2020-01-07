from rest_framework import status, permissions, generics, response

from session_auth.models import SessionMap
from core.utils.logs import get_logging_function


session_auth_log = get_logging_function('session_auth')


class Logout(generics.GenericAPIView):
    """
    This view deletes the cookie-based session authentication token from the
    database, thereby logging out the user

    Works only when authenticated
    """

    permission_classes = [permissions.IsAuthenticated, ]

    def get(self, request, *args, **kwargs):
        """
        View to serve GET requests
        :param request: the request that is to be responded to
        :param args: arguments
        :param kwargs: keyword arguments
        :return: the response for request
        """

        user = request.user
        session_key = request.session.session_key
        # This is a direct replacement for django.contrib.auth.logout()
        SessionMap.delete_session_map(request=request)
        session_auth_log(
            f'Successfully logged out of session {session_key}',
            'info',
            user
        )
        response_data = {
            'status': 'Successfully logged out',
        }
        return response.Response(
            data=response_data,
            status=status.HTTP_200_OK
        )
