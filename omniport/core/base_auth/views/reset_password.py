from rest_framework import status, generics, response

from base_auth.serializers.reset_password import (
    ResetPasswordSerializer,
)
from core.utils.logs import get_logging_function


base_auth_log = get_logging_function('base_auth')


class ResetPassword(generics.GenericAPIView):
    """
    This view, when responding to a GET request, shows the secret question for
    the user in question and, when responding to a POST request, takes the
    username, the secret_answer and the new password to reset it
    """

    serializer_class = ResetPasswordSerializer

    def post(self, request, *args, **kwargs):
        """
        View to serve POST requests
        :param request: the request that is to be responded to
        :param args: arguments
        :param kwargs: keyword arguments
        :return: the response for request
        """

        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.user
            new_password = serializer.validated_data.get('new_password')
            user.set_password(new_password)
            user.failed_reset_attempts = 0
            user.save()
            response_data = {
                'status': 'Successfully reset password.',
            }
            base_auth_log('Successfully reset password', 'info', user)
            return response.Response(
                data=response_data,
                status=status.HTTP_200_OK
            )
        else:
            response_data = {
                'errors': serializer.errors,
            }
            return response.Response(
                data=response_data,
                status=status.HTTP_400_BAD_REQUEST
            )