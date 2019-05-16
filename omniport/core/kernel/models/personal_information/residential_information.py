import swapper
from django.db import models

from kernel.models.personal_information.base import AbstractPersonalInformation


class AbstractResidentialInformation(AbstractPersonalInformation):
    """
    This model holds residential information about a person
    """

    residence = models.ForeignKey(
        to=swapper.get_model_name('kernel', 'Residence'),
        on_delete=models.CASCADE,
    )

    room_number = models.CharField(
        max_length=15,
    )

    class Meta:
        """
        Meta class for AbstractResidentialInformation
        """

        abstract = True

    def __str__(self):
        """
        Return the string representation of the model
        :return: the string representation of the model
        """

        person = self.person
        room_number = self.room_number
        residence = self.residence
        return f'{person} - {room_number}, {residence}'


class ResidentialInformation(AbstractResidentialInformation):
    """
    This class implements AbstractResidentialInformation
    """

    class Meta:
        """
        Meta class for ResidentialInformation
        """

        verbose_name_plural = 'residential information'
        swappable = swapper.swappable_setting('kernel',
                                              'ResidentialInformation')
