import swapper
from django.contrib.contenttypes import fields as contenttypes_fields
from django.db import models

from formula_one.models.base import Model


class AbstractDepartment(Model):
    """
    This class holds information about a department in the college
    """

    code = models.CharField(
        max_length=7,
        unique=True,
    )
    name = models.CharField(
        max_length=127,
    )

    location_information = contenttypes_fields.GenericRelation(
        to='formula_one.LocationInformation',
        related_query_name='department',
        content_type_field='entity_content_type',
        object_id_field='entity_object_id',
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
