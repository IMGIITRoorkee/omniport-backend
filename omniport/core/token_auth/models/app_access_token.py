import uuid
from django.db import models
from django.contrib.postgres import fields

from formula_one.models.base import Model

class AppAccessToken(Model):
    """
    Store the tokens which could be used by various apps to make an authenticated
    request
    """

    # AppAccessTokenAuthentication puts an instance of this on request.user, so
    # it has to answer what permissions, throttles and middleware ask of a user
    is_authenticated = True

    app_name = models.CharField(
        max_length=63, 
        blank=True,
        null=True,
    )

    description = models.TextField()

    permission_keys = fields.ArrayField(
        models.CharField(
            max_length=127,
            blank=False,
            null=False,
        )
    )

    access_token = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        unique=True,
        default=uuid.uuid4,
    )

    ip_address_regex = models.TextField()

    def __str__(self):
        """
        Return the string representation of the model
        :return: the string representation of the model
        """

        name = self.app_name
        return f'{name}'
