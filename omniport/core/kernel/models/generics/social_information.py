from django.contrib.contenttypes import fields as contenttypes_fields
from django.contrib.contenttypes import models as contenttypes_models
from django.db import models

from kernel.constants import social_links
from kernel.models.root import Model


class SocialLink(Model):
    """
    This model holds information about one social media link
    """

    site = models.CharField(
        max_length=7,
        choices=social_links.SOCIAL_SITES,
    )
    url = models.URLField(
        max_length=255,
        verbose_name='URL',
    )

    @property
    def site_logo(self):
        """
        Return the identifier from the Font Awesome library for this site
        :return: the identifier from the Font Awesome library for this site
        """

        return social_links.SOCIAL_SITE_ICONS[self.site]

    def __str__(self):
        """
        Return a string representation of the model
        :return: a string representation of the model
        """

        site = self.get_site_display()
        url = self.url

        return f'{site}: {url}'


class SocialInformation(Model):
    """
    This model holds information about how to contact 'any' sociable entity
    """

    links = models.ManyToManyField(
        to='SocialLink',
        blank=True,
    )

    # Relationship with the sociable entity
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
        Meta class for SocialInformation
        """

        verbose_name_plural = 'social information'

    def __str__(self):
        """
        Return the string representation of the model
        :return: the string representation of the model
        """

        entity = self.entity
        pk = self.id

        return f'{pk}: {entity}'
