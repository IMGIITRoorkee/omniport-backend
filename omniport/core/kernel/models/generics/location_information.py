from django.contrib.contenttypes import fields as contenttypes_fields
from django.contrib.contenttypes import models as contenttypes_models
from django.core.validators import RegexValidator
from django.db import models
from django_countries import fields as django_countries_fields

from kernel.models.root import Model


class LocationInformation(Model):
    """
    This model holds information about how to locate 'any' locatable entity
    """

    address = models.TextField()

    city = models.CharField(
        max_length=127,
    )
    state = models.CharField(
        max_length=127,
    )
    country = django_countries_fields.CountryField(
        blank_label='Country',
    )

    postal_code = models.IntegerField(
        validators=[
            RegexValidator(r'[0-9]{3,9}'),
        ],
        blank=True,
        null=True
    )

    latitude = models.DecimalField(
        max_digits=12,
        decimal_places=8,
        blank=True,
        null=True
    )
    longitude = models.DecimalField(
        max_digits=12,
        decimal_places=8,
        blank=True,
        null=True
    )

    # Relationship with the locatable entity
    entity_content_type = models.ForeignKey(
        to=contenttypes_models.ContentType,
        on_delete=models.CASCADE,
    )
    entity_object_id = models.PositiveIntegerField()
    entity = contenttypes_fields.GenericForeignKey(
        ct_field='entity_content_type',
        fk_field='entity_object_id',
    )

    class Meta:
        """
        Meta class for LocationInformation
        """

        verbose_name_plural = 'location information'

    def __str__(self):
        """
        Return the string representation of the model
        :return: the string representation of the model
        """

        city = self.city
        state = self.state
        country = self.country
        postal_code = self.postal_code
        return f'{city}, {state}, {country} - {postal_code}'
