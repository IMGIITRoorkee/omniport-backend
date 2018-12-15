from importlib import import_module

from django.conf import settings
from django.db import models

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

    ip_address = models.GenericIPAddressField()
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

    def clear_session(self):
        """
        Clear the associated session from the session store
        """

        SessionStore = import_module(settings.SESSION_ENGINE).SessionStore
        session = SessionStore(session_key=self.session_key)
        session.delete()

    def __str__(self):
        """
        Return the string representation of the model
        :return: the string representation of the model
        """

        session_key = self.session_key
        user = self.user
        return f'{session_key}: {user}'
