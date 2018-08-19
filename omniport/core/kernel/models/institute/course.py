import swapper
from django.core.validators import MinValueValidator
from django.db import models

from kernel.models.root import Model


class AbstractCourse(Model):
    """
    This class holds information about a course conducted by a department
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
    credits = models.IntegerField(
        validators=[
            MinValueValidator(limit_value=1),
        ],
    )

    prerequisites = models.ManyToManyField(
        to=swapper.get_model_name('kernel', 'Course'),
        blank=True,
        null=True,
    )

    class Meta:
        """
        Meta class for AbstractCourse
        """

        abstract = True

    def __str__(self):
        """
        Return the string representation of the model
        :return: the string representation of the model
        """

        code = self.code
        name = self.name
        return f'{code} - {name}'


class Course(AbstractCourse):
    """
    This class implements AbstractCourse
    """

    class Meta:
        """
        Meta class for Course
        """

        swappable = swapper.swappable_setting('kernel', 'Course')
