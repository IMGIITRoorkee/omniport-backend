from importlib import import_module

import requests
from django.conf import settings
from django.db import models
from user_agents import parse

from kernel.models.root import Model
from session_auth.constants import device_types


class SessionMap(Model):
    """
    This model stores all the sessions of a user
    """

    session_key = models.CharField(
        max_length=63,  # Actual length has been observed to be 32
        unique=True,
    )
    user = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        db_index=True,
    )

    ip_address = models.GenericIPAddressField(
        verbose_name='IP address',
    )
    location = models.CharField(
        max_length=255,
    )

    user_agent = models.CharField(
        max_length=255,
    )
    browser_family = models.CharField(
        max_length=31,
    )
    browser_version = models.CharField(
        max_length=31,
    )
    operating_system_family = models.CharField(
        max_length=31,
    )
    operating_system_version = models.CharField(
        max_length=31,
    )
    device_type = models.CharField(
        max_length=3,
        choices=device_types.DEVICE_TYPES,
    )

    @staticmethod
    def create_session_map(request):
        """
        Make a SessionMap instance that maps to a specific session key
        :param request: the request from which to extract all required data
        :return: the newly created SessionMap instance
        """

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
        session_map.user = request.user

        session_map.ip_address = ip_address
        session_map.location = location

        session_map.user_agent = user_agent_string
        session_map.browser_family = user_agent.browser.family
        session_map.browser_version = user_agent.browser.version_string
        session_map.operating_system_family = user_agent.os.family
        session_map.operating_system_version = user_agent.os.version_string
        session_map.device_type = device_type

        session_map.save()

    @staticmethod
    def delete_session_map(request):
        """
        Clear the associated session from the session store
        """

        session_key = request.session.session_key

        session_map = SessionMap.objects.get(session_key=session_key)
        session_map.delete()

        SessionStore = import_module(settings.SESSION_ENGINE).SessionStore
        session = SessionStore(session_key=session_key)
        session.delete()

    def __str__(self):
        """
        Return the string representation of the model
        :return: the string representation of the model
        """

        session_key = self.session_key
        user = self.user
        return f'{session_key}: {user}'
