import datetime

import swapper
from django.db import models

from kernel.constants import biological_information
from kernel.models.root import Model


class AbstractBiologicalInformation(Model):
    """
    This model holds biological information about a person
    """

    person = models.OneToOneField(
        to=swapper.get_model_name('kernel', 'Person'),
        on_delete=models.CASCADE,
    )

    date_of_birth = models.DateField()

    blood_group = models.CharField(
        max_length=3,
        choices=biological_information.BLOOD_GROUPS,
    )

    gender = models.CharField(
        max_length=7,
        choices=biological_information.GENDERS,
    )
    sex = models.CharField(
        max_length=7,
        choices=biological_information.SEXES,
    )
    pronoun = models.CharField(
        max_length=1,
        choices=biological_information.PRONOUNS,
    )

    impairment = models.CharField(
        max_length=1,
        choices=biological_information.IMPAIRMENTS,
    )

    class Meta:
        """
        Meta class for AbstractBiologicalInformation
        """

        abstract = True
        verbose_name_plural = 'biological information'

    @property
    def age_in_years(self):
        """
        Return the age of the person in years
        :return: the age of the person in years
        """

        timedelta = datetime.date.today() - self.date_of_birth
        years = int(timedelta.days / 365.2425)
        return years

    @property
    def age_in_days(self):
        """
        Return the age of the person in days
        :return: the age of the person in days
        """

        timedelta = datetime.date.today() - self.date_of_birth
        days = timedelta.days
        return days

    def __str__(self):
        """
        Return the string representation of the model
        :return: the string representation of the model
        """

        person = self.person
        date_of_birth = self.date_of_birth
        g = self.gender
        s = self.sex
        p = self.pronoun
        return f'{person} - {date_of_birth}, G({g}), S({s}), P({p})'


class BiologicalInformation(AbstractBiologicalInformation):
    """
    This class implements AbstractBiologicalInformation
    """

    class Meta:
        """
        Meta class for BiologicalInformation
        """

        swappable = swapper.swappable_setting('kernel', 'BiologicalInformation')
