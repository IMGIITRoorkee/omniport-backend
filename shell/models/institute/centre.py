from django.db import models

from kernel.models import AbstractCentre
from shell.constants import CENTRES


class Centre(AbstractCentre):
    """
    Make changes to AbstractCentre to suit IIT Roorkee
    """

    code = models.CharField(
        max_length=7,
        primary_key=True,
        unique=True,
        choices=CENTRES,
    )

    @property
    def name(self):
        """
        Return the name of the centre
        :return: the name of the centre
        """

        return self.get_code_display()
