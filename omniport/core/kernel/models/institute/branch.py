import swapper
from django.db import models
from django.contrib.contenttypes import fields as contenttypes_fields
from django.contrib.contenttypes import models as contenttypes_models

from formula_one.models.base import Model


class AbstractBranch(Model):
    """
    This class holds information about a branch offered by a department
    in the college
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
        max_length=7,
        unique=True,
    )
    name = models.CharField(
        max_length=127,
    )

    degree = models.ForeignKey(
        to=swapper.get_model_name('kernel', 'Degree'),
        on_delete=models.CASCADE,
    )

    semester_count = models.IntegerField(
        blank=True,
        null=True,
    )
    year_count = models.IntegerField(
        blank=True,
        null=True
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
