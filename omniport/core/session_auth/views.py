from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.renderers import TemplateHTMLRenderer, JSONRenderer
from rest_framework.response import Response

from session_auth.models import SessionMap
from session_auth.serializers import LoginSerializer


class Login(GenericAPIView):
    """
    This view takes the username and password and if correct, logs the user in
    via cookie-based session authentication
    """

    serializer_class = LoginSerializer
    renderer_classes = [
        TemplateHTMLRenderer,
        JSONRenderer,
    ]

    def get(self, request, *args, **kwargs):
        """
        View to serve GET requests
        :param request: the request that is to be responded to
        :param args: arguments
        :param kwargs: keyword arguments
        :return: the response for request
        """

        return Response(
            dict(),
            template_name='session_auth/login.html',
            status=status.HTTP_200_OK
        )

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

            # This is a direct replacement for django.contrib.auth.login()
            SessionMap.create_session_map(request=request, user=user)

            response = {
                'data': {
                    'type': 'message',
                    'attributes': {
                        'text': 'Successfully logged in',
                        'user': str(user),
                    },
                },
            }
            return Response(
                response,
                template_name='session_auth/login.html',
                status=status.HTTP_200_OK
            )
        else:
            response = {
                'errors': serializer.errors,
            }
            return Response(
                response,
                template_name='session_auth/login.html',
                status=status.HTTP_400_BAD_REQUEST
            )


class Logout(GenericAPIView):
    """
    This view deletes the cookie-based session authentication token from the
    database, thereby logging out the user

    Works only when authenticated
    """

    renderer_classes = [
        TemplateHTMLRenderer,
        JSONRenderer,
    ]

    def get(self, request, *args, **kwargs):
        """
        View to serve GET requests
        :param request: the request that is to be responded to
        :param args: arguments
        :param kwargs: keyword arguments
        :return: the response for request
        """

        # This is a direct replacement for django.contrib.auth.logout()
        SessionMap.delete_session_map(request=request)

        response = {
            'data': {
                'type': 'message',
                'attributes': {
                    'text': 'Successfully logged out',
                },
            },
        }
        return Response(
            response,
            template_name='session_auth/logout.html',
            status=status.HTTP_200_OK
        )
