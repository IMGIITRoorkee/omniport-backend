import swapper
from django.db import models

from kernel.models.root import Model


class AbstractFinancialInformation(Model):
    """
    This model holds financial information about a person
    """

    person = models.OneToOneField(
        to=swapper.get_model_name('kernel', 'Person'),
        on_delete=models.CASCADE,
    )

    local_bank = models.CharField(
        max_length=63,
        blank=True,
    )
    local_bank_account_number = models.CharField(
        max_length=31,
        blank=True,
    )
    annual_income = models.DecimalField(
        max_digits=31,
        decimal_places=2,
        blank=True,
        null=True,
    )

    class Meta:
        """
        Meta class for AbstractFinancialInformation
        """

        abstract = True
        verbose_name_plural = 'financial information'

    def __str__(self):
        """
        Return the string representation of the model
        :return: the string representation of the model
        """

        person = self.person
        local_bank = self.local_bank
        local_bank_account_number = self.local_bank_account_number
        return f'{person} - {local_bank}, {local_bank_account_number}'


class FinancialInformation(AbstractFinancialInformation):
    """
    This class implements AbstractFinancialInformation
    """

    class Meta:
        """
        Meta class for FinancialInformation
        """

        swappable = swapper.swappable_setting('kernel', 'FinancialInformation')
