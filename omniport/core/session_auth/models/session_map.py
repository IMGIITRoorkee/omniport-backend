from django.conf import settings
from django.contrib.auth import logout, login
from django.db import models

from formula_one.models.base import Model
from session_auth.constants import device_types
from session_auth.utils.ip_address import get_location
from session_auth.utils.user_agent import get_agent_information


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
        max_length=511,
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
    def create_session_map(request, user, new=True):
        """
        Make a SessionMap instance that maps to a specific session key
        :param request: the request from which to extract all required data
        :param user: the user to log in on the request
        :param new: whether the user has just logged in or was already
        :return: the newly created SessionMap instance
        """

        # Set the cookie and initiate the session
        if new:
            login(request, user)

        # Store the additional information in the relational database
        session_map = SessionMap()
        session_map.session_key = request.session.session_key
        session_map.user = request.user

        # Get the location from IP address
        ip_address = request.source_ip_address
        location = get_location(ip_address)
        session_map.ip_address = ip_address
        session_map.location = location

        # Get the browser, operating system and device from the user-agent
        user_agent_string = request.META.get('HTTP_USER_AGENT', 'Unknown')
        (browser, os, device_type) = get_agent_information(user_agent_string)
        session_map.user_agent = user_agent_string
        session_map.browser_family = browser.family
        session_map.browser_version = browser.version_string
        session_map.operating_system_family = os.family
        session_map.operating_system_version = os.version_string
        session_map.device_type = device_type

        session_map.save()

    @staticmethod
    def delete_session_map(request):
        """
        Delete the SessionMap instance associated with the request and clear the
        associated session from the session store
        :param request: the request that is to be stripped of authentication
        """

        # Get the additional information from the relational database
        session_key = request.session.session_key
        session_map = SessionMap.objects.get(session_key=session_key)
        session_map.delete()

        # Delete the cookie and flush the session
        logout(request)

    def __str__(self):
        """
        Return the string representation of the model
        :return: the string representation of the model
        """

        session_key = self.session_key
        user = self.user
        return f'{session_key}: {user}'
