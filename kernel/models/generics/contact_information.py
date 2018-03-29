from django.contrib.contenttypes import fields as contenttypes_fields
from django.contrib.contenttypes import models as contenttypes_models
from django.db import models

from kernel.models.root import Model


class ContactInformation(Model):
    """
    This model holds information about how to contact 'any' contactable entity
    """

    primary_phone_number = models.CharField(
        max_length=15,
        unique=True,
    )
    secondary_phone_number = models.CharField(
        max_length=15,
        unique=True,
        blank=True,
        null=True,
    )

    email_address = models.EmailField(
        unique=True,
        blank=True,
        null=True,
    )
    email_address_verified = models.BooleanField(
        default=False,
    )

    institute_webmail_address = models.EmailField(
        unique=True,
        blank=True,
        null=True,
    )

    # Relationship with the contactable entity
    entity_content_type = models.ForeignKey(
        to=contenttypes_models.ContentType,
        on_delete=models.CASCADE,
    )
    entity_object_id = models.PositiveIntegerField()
    entity = contenttypes_fields.GenericForeignKey(
        'entity_content_type',
        'entity_object_id'
    )

    class Meta:
        """
        Meta class for ContactInformation
        """

        verbose_name_plural = 'contact information'

    def get_one_true_email_address(self, check_verified=True):
        """
        Return the populated email address or None
        :return: the populated email address if it exists, None otherwise
        """

        if bool(self.email_address):
            if not check_verified or self.email_address_verified:
                return self.email_address

        if bool(self.institute_webmail_address):
            return self.institute_webmail_address

        return None

    def __str__(self):
        """
        Return the string representation of the model
        :return: the string representation of the model
        """

        phone_number = self.primary_phone_number
        email_address = self.get_one_true_email_address()
        return f'{phone_number}, {email_address}'
