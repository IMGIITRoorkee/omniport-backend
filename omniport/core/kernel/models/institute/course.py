import swapper
from django.core.validators import MinValueValidator
from django.db import models
from django.contrib.contenttypes import fields as contenttypes_fields
from django.contrib.contenttypes import models as contenttypes_models

from formula_one.models.base import Model


class AbstractCourse(Model):
    """
    This class holds information about a course conducted by a department
    """

    # Relationship with the department or center entity
    _limits = models.Q(
        app_label=swapper.get_model_name('kernel', 'Department').split('.')[0],
        model='department',
    ) | models.Q(
        app_label=swapper.get_model_name('kernel', 'Centre').split('.')[0],
        model='centre',
    )
    entity_content_type = models.ForeignKey(
        to=contenttypes_models.ContentType,
        on_delete=models.CASCADE,
        limit_choices_to=_limits,
    )
    entity_object_id = models.BigIntegerField()
    content_object = contenttypes_fields.GenericForeignKey(
        ct_field='entity_content_type',
        fk_field='entity_object_id',
    )

    code = models.CharField(
        max_length=15,
        unique=True,
    )
    name = models.CharField(
        max_length=127,
    )
    credits = models.IntegerField(
        validators=[
            MinValueValidator(limit_value=0),
        ],
    )

    prerequisites = models.ManyToManyField(
        to=swapper.get_model_name('kernel', 'Course'),
        blank=True,
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

    @property
    def department(self):
        """
        Return the department of the branch
        :return: the department object
        """

        if self.entity_content_type.name == 'centre':
            Class = swapper.load_model('shell', 'Centre')
        else:
            Class = swapper.load_model('shell', 'Department')

        department = Class.objects.get(id=self.entity_object_id)

        return department

class Course(AbstractCourse):
    """
    This class implements AbstractCourse
    """

    class Meta:
        """
        Meta class for Course
        """

        swappable = swapper.swappable_setting('kernel', 'Course')
