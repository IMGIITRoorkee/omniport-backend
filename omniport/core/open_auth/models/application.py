import swapper
from django.contrib.postgres import fields
from django.db import models
from oauth2_provider.models import AbstractApplication

from kernel.models.root import Model
from kernel.utils.upload_to import UploadTo
from open_auth.constants import data_points as data_point_choices


class Application(AbstractApplication, Model):
    """
    Extends the OAuth2 AbstractApplication model and replaces the default one
    supplied in order to add extended information and functionality beyond that
    provided by the package
    """

    logo = models.ImageField(
        upload_to=UploadTo('open_auth', 'application_logos'),
        max_length=255,
        blank=True,
        null=True,
    )

    description = models.TextField()

    agrees_to_terms = models.BooleanField(
        default=False,
    )
    is_approved = models.BooleanField(
        default=False,
    )

    team_members = models.ManyToManyField(
        to=swapper.get_model_name('kernel', 'Person'),
        blank=True,
    )

    data_points = fields.ArrayField(
        models.CharField(
            max_length=127,
            choices=data_point_choices.DATA_POINTS,
        )
    )

    def __str__(self):
        """
        Return the string representation of the model
        :return: the string representation of the model
        """

        name = self.name
        return f'{name}'
