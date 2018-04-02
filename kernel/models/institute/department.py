import swapper
from django.db import models

from kernel.models.root import Model


class AbstractDepartment(Model):
    """
    This class holds information about a department in the college
    """

    code = models.CharField(
        max_length=7,
        primary_key=True,
        unique=True,
    )
    name = models.CharField(
        max_length=127,
    )

    class Meta:
        """
        Meta class for AbstractDepartment
        """

        abstract = True

    def __str__(self):
        """
        Return a string representation of the model
        :return: a string representation of the model
        """

        name = self.name
        return f'{name}'


class Department(AbstractDepartment):
    """
    This class implements AbstractDepartment
    """

    class Meta:
        """
        Meta class for Department
        """

        swappable = swapper.swappable_setting('kernel', 'Department')
