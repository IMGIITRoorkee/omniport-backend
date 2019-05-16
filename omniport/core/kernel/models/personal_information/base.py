import swapper
from django.db import models

from formula_one.models.base import Model


class AbstractPersonalInformation(Model):
    """
    This model holds information about a person
    """

    person = models.OneToOneField(
        to=swapper.get_model_name('kernel', 'Person'),
        on_delete=models.CASCADE,
    )

    class Meta:
        """
        Meta class for AbstractPersonalInformation
        """

        abstract = True
