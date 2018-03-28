import datetime

from django.db import models


class PeriodMixin:
    """
    This mixin adds information about the start and end of any entity's
    active period
    """

    start_date = models.DateField()
    # A blank end date is considered active
    end_date = models.DateField(
        blank=True,
        null=True,
    )

    @property
    def is_active(self):
        """
        Return whether the entity is currently active
        :return: True if start date has passed and end date has not
        """

        today = datetime.date.today()
        if self.end_date is not None:
            return self.start_date < today < self.end_date
        else:
            return self.start_date < today

    @property
    def is_yet_to_begin(self):
        """
        Return whether the period is yet to begin
        :return: True if the start date is later than today, False otherwise
        """

        today = datetime.date.today()
        return self.start_date > today

    @property
    def has_already_ended(self):
        """
        Return whether the period has already over
        :return: True if today is later than the end date, False otherwise
        """

        today = datetime.date.today()
        if self.end_date is not None:
            return self.end_date < today
        else:
            return False

    @property
    def start_year(self):
        """
        Return the year of the start date
        :return: the year of the start date
        """

        return self.start_date.year

    @property
    def end_year(self):
        """
        Return the year of the end date
        :return: the year of the end date
        """

        if self.has_already_ended:
            return self.end_date.year
        else:
            raise ValueError('Period has not ended')
