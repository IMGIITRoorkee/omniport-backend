from django.db import models

from kernel.models import AbstractPoliticalInformation


class PoliticalInformation(AbstractPoliticalInformation):
    """
    Make changes to AbstractPoliticalInformation to suit IIT Roorkee
    """

    aadhaar_card_number = models.CharField(
        max_length=12,
        blank=True,
    )

    class Meta:
        """
        Meta class for PoliticalInformation
        """

        verbose_name_plural = 'political information'

    def __str__(self):
        """
        Return the string representation of the model
        :return: the string representation of the model
        """

        person = self.person
        nationality = self.nationality
        aadhaar_card_number = self.aadhaar_card_number
        return f'{person} - {nationality}, {aadhaar_card_number}'
