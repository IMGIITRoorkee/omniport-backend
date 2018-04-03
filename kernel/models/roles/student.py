import swapper
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from kernel.mixins.period_mixin import PeriodMixin
from kernel.models.root import Model


class AbstractStudent(PeriodMixin, Model):
    """
    This model holds information pertaining to a student
    """

    person = models.ForeignKey(
        to=swapper.get_model_name('kernel', 'Person'),
        on_delete=models.CASCADE,
    )

    enrolment_number = models.CharField(
        max_length=15,
        primary_key=True,
        unique=True,
    )

    branch = models.ForeignKey(
        to=swapper.get_model_name('kernel', 'Branch'),
        on_delete=models.CASCADE,
    )

    current_year = models.IntegerField()
    current_semester = models.IntegerField()
    current_cgpa = models.DecimalField(
        max_digits=5,
        decimal_places=3,
        validators=[
            MaxValueValidator(10.000),
            MinValueValidator(00.000),
        ],
        blank=True,
        null=True,
    )

    class Meta:
        """
        Meta class for AbstractStudent
        """

        abstract = True

    @property
    def is_alumnus(self):
        """
        Return whether or not the student is an alumnus
        :return: True if the role period has already ended, False otherwise
        """

        return self.has_already_ended

    @property
    def is_pre_freshman(self):
        """
        Return whether or not the student is a pre-freshman
        :return: True if the role period is yet to begin, False otherwise
        """

        return self.is_yet_to_begin

    def __str__(self):
        """
        Return the string representation of the model
        :return: the string representation of the model
        """

        enrolment_number = self.enrolment_number
        person = self.person
        branch = self.branch
        return f'{enrolment_number} - {person}, {branch}'


class Student(AbstractStudent):
    """
    This class implements AbstractStudent
    """

    class Meta:
        """
        Meta class for Student
        """

        swappable = swapper.swappable_setting('kernel', 'Student')
