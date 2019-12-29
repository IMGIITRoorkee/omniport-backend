import random
import string

from rest_framework import generics, response, status
from rest_framework.decorators import api_view

from base_auth.models import User
from base_auth.redisdb.recover_token import push, retreive, delete
from emails.actions import email_push


class RecoverPassword(generics.GenericAPIView):
    """
    This view when responding to a GET request, generates password recovery token
    and sends mail to the concerned user. and when responding to a POST request
    changes the password of the user.
    """

    def get(self, request):
        """
        View to serve GET requests
        :param request: the request this is to be responded to
        :return: the response for request
        """

        username = request.GET.get('username', None)

        if not username:
            return response.Response(
                data="Please provide the username",
                status=status.HTTP_400_BAD_REQUEST,
            )

        user = User.objects.get(username=username)
        person = user.person

        while True:
            recovery_token = "".join(random.choice(string.ascii_letters + string.digits)
                                     for i in range(20))
            res = push(recovery_token, user.id)
            if res:
                break

        url = f"http://localhost.com/?{recovery_token}"

        subject = "Channel-i account password reset"
        body = f'Please visit {url} for password reset.'

        try:
            email_push(subject, body, None, 1, True, [person.id], 'IMG', 'IMG.com')
        except:
            return response.Response(
                data="There was some trouble sending the email. Please retry after some time.",
                status=status.HTTP_417_EXPECTATION_FAILED,
            )

        return response.Response(
            data="Email sent successfully",
            status=status.HTTP_200_OK,
        )

    def post(self, request):
        """
        View to serve POST requests
        :param request: the request this is to be responded to
        :return: the response for request
        """

        recovery_token = request.POST.get('recovery_token', None)
        username = request.POST.get('username', None)
        new_password = request.POST.get('new_password', None)

        user = retreive(recovery_token)
        if not user:
            return response.Response(
                data="This recovery token is  wrong",
                status=status.HTTP_404_NOT_FOUND,
            )
        if username != user.username:
            return response.Response(
                data="The username provided is incorrect",
                status=status.HTTP_403_FORBIDDEN,
            )
        if not new_password:
            return response.Response(
                data="Please provide new Password",
                status=status.HTTP_400_BAD_REQUEST,
            )
        user.set_password(new_password)
        user.save()
        delete(recovery_token)

        return response.Response(
            data="Password changed successfully",
            status=status.HTTP_200_OK,
        )

@api_view(('GET', ))
def verify_recovery_token(request):
    """
    This view serves GET request, and returns the username of the user
    if recovery token exists and error otherwise.
    :param request: the request that is being responded to
    :return: the response to the request.
    """

    recovery_token = request.GET.get('recovery_token', None)

    if not recovery_token:
        return response.Response(
            data="Please send the recovery token",
            status=status.HTTP_400_BAD_REQUEST,
        )
    user = retreive(recovery_token)

    if not user:
        return response.Response(
            data="Invalid recovery token",
            status=status.HTTP_404_NOT_FOUND,
        )

    response_data = {'username':user.username}

    return response.Response(
        data=response_data,
        status=status.HTTP_200_OK,
    )
