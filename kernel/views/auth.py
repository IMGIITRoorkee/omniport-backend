import random
import string

from django.contrib.auth import authenticate, login, logout
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from kernel.errors.auth import (
    INCORRECT_CREDENTIALS,
    USER_DOES_NOT_EXIST,
    RESET_ATTEMPTS_EXHAUSTED,
)
from kernel.errors.forms import INCOMPLETE_DATA
from kernel.managers.get_user import get_user
from kernel.models.auth import User
from kernel.permissions.has_lockpicking_rights import HasLockpickingRights
from kernel.permissions.is_not_authenticated import IsNotAuthenticated


class Login(APIView):
    """
    This view takes the username and password and if correct, logs the user in
    via cookie-based session authentication

    Works only when not authenticated
    """

    permission_classes = (IsNotAuthenticated,)

    def post(self, request, *args, **kwargs):
        """
        View to serve POST requests
        :param request: the request that is to be responded to
        :param args: arguments
        :param kwargs: keyword arguments
        :return: the response for request
        """

        errors = list()

        username = request.data.get('username', None)
        password = request.data.get('password', None)

        if username is not None and password is not None:
            user = authenticate(
                request,
                username=username,
                password=password
            )
            if user is not None:
                login(request, user)
                response = {
                    'data': {
                        'type': 'message',
                        'attributes': {
                            'text': 'Successfully logged in',
                            'user': str(user),
                        },
                    },
                }
                return Response(response)
            else:
                errors.append(INCORRECT_CREDENTIALS)
        else:
            errors.append(INCOMPLETE_DATA)

        response = {
            'errors': errors,
        }
        return Response(response, status=status.HTTP_400_BAD_REQUEST)


class ChangePassword(APIView):
    """
    This view takes the old password and the new password and if the old
    password is correct, changes the password to the new one

    Works only when authenticated
    """

    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        """
        View to serve POST requests
        :param request: the request that is to be responded to
        :param args: arguments
        :param kwargs: keyword arguments
        :return: the response for request
        """

        errors = list()

        old_password = request.data.get('old_password', None)
        new_password = request.data.get('new_password', None)

        if old_password is not None and new_password is not None:
            user = request.user
            if user.check_password(old_password):
                user.set_password(new_password)
                user.save()
                response = {
                    'data': {
                        'type': 'message',
                        'attributes': {
                            'text': 'Successfully changed password',
                        },
                    },
                }
                return Response(response)
            else:
                errors.append(INCORRECT_CREDENTIALS)
        else:
            errors.append(INCOMPLETE_DATA)

        response = {
            'errors': errors,
        }
        return Response(response, status=status.HTTP_400_BAD_REQUEST)


class ResetPassword(APIView):
    """
    This view, when responding to a GET request, shows the secret question for
    the user in question and, when responding to a POST request, takes the
    username, the secret_answer and the new password to reset it

    Works only when not authenticated
    """

    permission_classes = (IsNotAuthenticated,)

    def get(self, request, *args, **kwargs):
        """
        View to serve GET requests
        :param request: the request that is to be responded to
        :param args: arguments
        :param kwargs: keyword arguments
        :return: the response for request
        """

        errors = list()

        username = request.query_params.get('username', None)

        if username is not None:
            try:
                user = get_user(username)
                secret_question = user.secret_question
                response = {
                    'data': {
                        'type': 'secret_question',
                        'attributes': {
                            'text': secret_question,
                        },
                    },
                }
                return Response(response)
            except User.DoesNotExist:
                errors.append(USER_DOES_NOT_EXIST)
        else:
            errors.append(INCOMPLETE_DATA)

        response = {
            'errors': errors,
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

        errors = list()

        username = request.data.get('username', None)
        secret_answer = request.data.get('secret_answer', None)
        new_password = request.data.get('new_password', None)

        if (
                username is not None
                and secret_answer is not None
                and new_password is not None
        ):
            try:
                user = get_user(username)
                if user.failed_reset_attempts < 3:
                    if user.check_secret_answer(secret_answer):
                        user.set_password(new_password)
                        user.save()
                        response = {
                            'data': {
                                'type': 'message',
                                'attributes': {
                                    'text': 'Successfully changed password',
                                },
                            },
                        }
                        return Response(response)
                    else:
                        errors.append(INCORRECT_CREDENTIALS)
                else:
                    errors.append(RESET_ATTEMPTS_EXHAUSTED)
            except User.DoesNotExist:
                errors.append(USER_DOES_NOT_EXIST)
        else:
            errors.append(INCOMPLETE_DATA)

        response = {
            'errors': errors,
        }
        return Response(response, status=status.HTTP_400_BAD_REQUEST)


class Lockpick(APIView):
    """
    This view takes the username and optionally, a new password and if an
    authorised user is logged in, changes the password for the user with the
    given username to the new one. If no password is specified a random one with
    eight letters is created and shown to the person resetting it

    Works only when a person with lockpicking rights is logged in
    """

    permission_classes = (IsAuthenticated, HasLockpickingRights,)

    def post(self, request, *args, **kwargs):
        """
        View to serve POST requests
        :param request: the request that is to be responded to
        :param args: arguments
        :param kwargs: keyword arguments
        :return: the response for request
        """

        errors = list()

        username = request.data.get('username', None)
        new_password = request.data.get('new_password', None)

        if username is not None:
            try:
                user = get_user(username)
                if new_password is None:
                    allowed_chars = string.ascii_uppercase + string.digits
                    password_length = 8
                    new_password = ''.join(
                        random.SystemRandom().choice(allowed_chars)
                        for _ in range(password_length)
                    )
                user.set_password(new_password)
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
                return Response(response)
            except User.DoesNotExist:
                errors.append(USER_DOES_NOT_EXIST)
        else:
            errors.append(INCOMPLETE_DATA)

        response = {
            'errors': errors,
        }
        return Response(response, status=status.HTTP_400_BAD_REQUEST)


class Logout(APIView):
    """
    This view deletes the cookie-based session authentication token from the
    database, thereby logging out the user

    Works only when authenticated
    """

    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        """
        View to serve GET requests
        :param request: the request that is to be responded to
        :param args: arguments
        :param kwargs: keyword arguments
        :return: the response for request
        """

        logout(request)
        response = {
            'data': {
                'type': 'message',
                'attributes': {
                    'text': 'Successfully logged out',
                },
            },
        }
        return Response(response)
