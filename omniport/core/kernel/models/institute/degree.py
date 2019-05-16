import swapper
from django.db import models

from formula_one.models.base import Model
from kernel.constants import graduations


class AbstractDegree(Model):
    """
    This model holds information about a degree offered by the institute
    """

    code = models.CharField(
        max_length=7,
        unique=True,
    )
    name = models.CharField(
        max_length=127,
    )

    graduation = models.CharField(
        max_length=3,
        choices=graduations.GRADUATIONS,
    )

    class Meta:
        """
        Meta class for AbstractDegree
        """

        abstract = True

    def __str__(self):
        """
        Return the string representation of the model
        :return: the string representation of the model
        """

        name = self.name
        graduation = self.graduation
        return f'{name} ({graduation})'


class Degree(AbstractDegree):
    """
    This class implements AbstractDegree
    """

    class Meta:
        """
        Meta class for AbstractDegree
        """

        swappable = swapper.swappable_setting('kernel', 'Degree')
