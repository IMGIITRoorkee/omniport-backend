import requests
from django.contrib.auth import login
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.renderers import TemplateHTMLRenderer, JSONRenderer
from rest_framework.response import Response
from user_agents import parse

from session_auth.constants import device_types
from session_auth.models.session import SessionMap
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
            login(request, user)

            # Get the location from IP address
            ip_address = request.source_ip_address
            fields = ','.join([
                'status',
                'message',
                'city',
                'country',
                'countryCode',
            ])
            response = requests.get(
                url=f'http://ip-api.com/json/{ip_address}',
                params={'fields': fields},
            )
            response = response.json()
            if response.pop('status') == 'success':
                location = ', '.join([
                    response.get('city'),
                    response.get('country'),
                    response.get('countryCode'),
                ])
            else:
                if response.get('message') == 'private range':
                    location = 'Intranet'
                elif response.get('message') == 'reserved range':
                    location = 'Reserved'
                else:
                    location = 'The Void'

            # Get the browser, operating system and device from the user-agent
            user_agent_string = request.META['HTTP_USER_AGENT']
            user_agent = parse(user_agent_string)
            if user_agent.is_pc:
                device_type = device_types.COMPUTER
            elif user_agent.is_tablet:
                device_type = device_types.TABLET
            elif user_agent.is_mobile:
                device_type = device_types.MOBILE
            else:
                device_type = device_types.UNKNOWN

            # Store the additional information in the relational database
            session_map = SessionMap()

            session_map.session_key = request.session.session_key
            session_map.user = user

            session_map.ip_address = ip_address
            session_map.location = location

            session_map.user_agent = user_agent_string
            session_map.browser_family = user_agent.browser.family
            session_map.browser_version = user_agent.browser.version_string
            session_map.operating_system_family = user_agent.os.family
            session_map.operating_system_version = user_agent.os.version_string
            session_map.device_type = device_type

            session_map.save()

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

        session_key = request.session.session_key
        session = SessionMap.objects.get(session_key=session_key)
        session.clear_session()
        session.delete()

        request.session.flush()

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
