import swapper
from django.db import models

from kernel.models.root import Model


class AbstractResidentialInformation(Model):
    """
    This model holds residential information about a person
    """

    person = models.OneToOneField(
        to=swapper.get_model_name('kernel', 'Person'),
        on_delete=models.CASCADE,
    )

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
        return f'{person}'


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
