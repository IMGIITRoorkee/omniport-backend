import swapper
from django.contrib.contenttypes import fields as contenttypes_fields
from django.db import models

from formula_one.models.base import Model


class AbstractResidence(Model):
    """
    This class holds information about a residence in the college
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
        related_query_name='residence',
        content_type_field='entity_content_type',
        object_id_field='entity_object_id',
    )

    class Meta:
        """
        Meta class for AbstractResidence
        """

        abstract = True

    def __str__(self):
        """
        Return the string representation of the model
        :return: the string representation of the model
        """

        name = self.name
        return f'{name}'


class Residence(AbstractResidence):
    """
    This class implements AbstractResidence
    """

    class Meta:
        """
        Meta class for Residence
        """

        swappable = swapper.swappable_setting('kernel', 'Residence')
