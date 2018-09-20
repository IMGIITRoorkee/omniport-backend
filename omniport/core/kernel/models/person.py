import swapper
from django.contrib.contenttypes import fields as contenttypes_fields
from django.db import models

from kernel.models.root import Model
from kernel.utils.upload_to import UploadTo


def upload_to():
    """
    This dummy function must live on because its name has been etched into a
    migration forever

    Removal will result in an exception.
    """

    pass


class AbstractPerson(Model):
    """
    This model describes a person who uses Omniport
    """

    short_name = models.CharField(
        max_length=63,
        blank=True,
    )
    full_name = models.CharField(
        max_length=255,
    )

    # Relationships with other people
    parents = models.ManyToManyField(
        to=swapper.get_model_name('kernel', 'Person'),
        related_name='children',
        blank=True,
    )
    local_guardians = models.ManyToManyField(
        to=swapper.get_model_name('kernel', 'Person'),
        related_name='wards',
        blank=True,
    )
    spouses = models.ManyToManyField(
        to='self',
        symmetrical=True,
        blank=True,
    )

    contact_information = contenttypes_fields.GenericRelation(
        to='ContactInformation',
        related_query_name='person',
        content_type_field='entity_content_type',
        object_id_field='entity_object_id',
    )
    social_information = contenttypes_fields.GenericRelation(
        to='SocialInformation',
        related_query_name='person',
        content_type_field='entity_content_type',
        object_id_field='entity_object_id',
    )
    location_information = contenttypes_fields.GenericRelation(
        to='LocationInformation',
        related_query_name='person',
        content_type_field='entity_content_type',
        object_id_field='entity_object_id',
    )

    display_picture = models.ImageField(
        upload_to=UploadTo('kernel', 'display_pictures'),
        max_length=255,
        blank=True,
        null=True,
    )

    class Meta:
        """
        Meta class for AbstractPerson
        """

        abstract = True

    def get_short_name(self):
        """
        Return the short name of the person
        :return: the short name of the person, or full name if none found
        """

        if self.short_name:
            return self.short_name
        else:
            return self.get_full_name()

    def get_full_name(self):
        """
        Return the full name of the person
        :return: the full name of the person
        """

        return self.full_name

    def __str__(self):
        """
        Return the string representation of the model
        :return: the string representation of the model
        """

        return self.get_full_name()


class Person(AbstractPerson):
    """
    This class implements AbstractPerson
    """

    class Meta:
        """
        Meta class for Person
        """

        verbose_name_plural = 'people'
        swappable = swapper.swappable_setting('kernel', 'Person')
