import swapper
from django.db import models

from kernel.models.root import Model


class AbstractBranch(Model):
    """
    This class holds information about a branch offered by a department
    in the college
    """

    department = models.ForeignKey(
        to=swapper.get_model_name('kernel', 'Department'),
        on_delete=models.CASCADE,
    )

    code = models.CharField(
        max_length=7,
        primary_key=True,
        unique=True,
    )
    name = models.CharField(
        max_length=127,
    )

    degree = models.CharField(
        max_length=63,
    )
    graduation = models.CharField(
        max_length=63,
    )
    semester_count = models.IntegerField(
        blank=True,
        null=True,
    )

    class Meta:
        """
        Meta class for AbstractBranch
        """

        abstract = True

    def __str__(self):
        """
        Return a string representation of the model
        :return: a string representation of the model
        """

        department = self.department
        name = self.name
        return f'{name}, {department}'


class Branch(AbstractBranch):
    """
    This class implements AbstractBranch
    """

    class Meta:
        """
        Meta class for Branch
        """

        verbose_name_plural = 'branches'
        swappable = swapper.swappable_setting('kernel', 'Branch')
