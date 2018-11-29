import swapper
from django.db import models

from kernel.mixins.period_mixin import PeriodMixin
from kernel.models.root import Model


class AbstractFacultyMember(PeriodMixin, Model):
    """
    This model holds information pertaining to a faculty member
    """

    person = models.OneToOneField(
        to=swapper.get_model_name('kernel', 'Person'),
        on_delete=models.CASCADE,
    )

    designation = models.CharField(
        max_length=63,
    )
    department = models.ForeignKey(
        to=swapper.get_model_name('kernel', 'Department'),
        on_delete=models.CASCADE,
    )

    class Meta:
        """
        Meta class for AbstractFacultyMember
        """

        abstract = True

    @property
    def is_retired(self):
        """
        Return whether or not the faculty member is retired
        :return: True if the role period has already ended, False otherwise
        """

        return self.has_already_ended

    def __str__(self):
        """
        Return the string representation of the model
        :return: the string representation of the model
        """

        person = self.person
        designation = self.designation
        department = self.department
        return f'{person} - {designation}, {department}'


class FacultyMember(AbstractFacultyMember):
    """
    This class implements AbstractFacultyMember
    """

    class Meta:
        """
        Meta class for FacultyMember
        """

        swappable = swapper.swappable_setting('kernel', 'FacultyMember')
