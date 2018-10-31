from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from kernel.permissions.has_lockpicking_rights import HasLockpickingRights
from kernel.serializers.auth import (
    UserRetrievalSerializer,
    ChangePasswordSerializer,
    ResetPasswordSerializer,
    LockpickingSerializer,
)


class ChangePassword(GenericAPIView):
    """
    This view takes the old password and the new password and if the old
    password is correct, changes the password to the new one

    Works only when authenticated
    """

    permission_classes = (IsAuthenticated,)

    serializer_class = ChangePasswordSerializer

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
            new_password = serializer.validated_data.get('new_password')
            user = request.user
            user.set_password(new_password)
            user.failed_reset_attempts = 0
            user.save()
            response = {
                'data': {
                    'type': 'message',
                    'attributes': {
                        'text': 'Successfully changed password',
                    },
                },
            }
            return Response(response, status=status.HTTP_200_OK)
        else:
            response = {
                'errors': serializer.errors,
            }
            return Response(response, status=status.HTTP_400_BAD_REQUEST)


class ResetPassword(GenericAPIView):
    """
    This view, when responding to a GET request, shows the secret question for
    the user in question and, when responding to a POST request, takes the
    username, the secret_answer and the new password to reset it
    """

    serializer_class = ResetPasswordSerializer

    def get(self, request, *args, **kwargs):
        """
        View to serve GET requests
        :param request: the request that is to be responded to
        :param args: arguments
        :param kwargs: keyword arguments
        :return: the response for request
        """

        username = request.query_params.get('username', None)
        serializer = UserRetrievalSerializer(data={'username': username})
        if serializer.is_valid():
            user = serializer.user
            secret_question = user.secret_question
            response = {
                'data': {
                    'type': 'secret_question',
                    'attributes': {
                        'text': secret_question,
                    },
                },
            }
            return Response(response, status=status.HTTP_200_OK)
        else:
            response = {
                'errors': serializer.errors,
            }
            return Response(response, status=status.HTTP_400_BAD_REQUEST)

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
            response = {
                'data': {
                    'type': 'message',
                    'attributes': {
                        'text': 'Successfully reset password',
                    },
                },
            }
            return Response(response, status=status.HTTP_200_OK)
        else:
            response = {
                'errors': serializer.errors,
            }
            return Response(response, status=status.HTTP_400_BAD_REQUEST)


class Lockpick(GenericAPIView):
    """
    This view takes the username and optionally, a new password and if an
    authorised user is logged in, changes the password for the user with the
    given username to the new one. If no password is specified a random one with
    eight letters is created and shown to the person resetting it

    Works only when a person with lockpicking rights is logged in
    """

    permission_classes = (IsAuthenticated, HasLockpickingRights,)

    serializer_class = LockpickingSerializer

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
            response = {
                'data': {
                    'type': 'message',
                    'attributes': {
                        'text': 'Successfully changed password',
                        'password': new_password,
                    },
                },
            }
            return Response(response, status=status.HTTP_200_OK)
        else:
            response = {
                'errors': serializer.errors,
            }
            return Response(response, status=status.HTTP_400_BAD_REQUEST)
