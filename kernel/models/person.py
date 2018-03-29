import swapper
from django.db import models

from kernel.models.root import Model


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

    class Meta:
        """
        Meta class for AbstractPerson
        """

        abstract = True
        verbose_name_plural = 'people'

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

        swappable = swapper.swappable_setting('kernel', 'Person')
