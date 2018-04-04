import datetime

from django.db import models
from django.db.models import Q, Model


class PeriodMixin(Model):
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

    class Meta:
        """
        Meta class for PeriodMixin
        """

        abstract = True

    @classmethod
    def all_filter_will_be_active(cls):
        """
        Return a query set of objects filtering only the to-be-active ones
        :return: a query set of to-be-active objects
        """

        if hasattr(cls, 'objects'):
            today = datetime.date.today()
            return cls.objects.all().filter(start_date__gt=today)
        else:
            raise AttributeError('Class does not have attribute \'objects\'')

    @classmethod
    def all_filter_active(cls):
        """
        Return a query set of objects filtering only the currently active ones
        :return: a query set of currently active objects
        """

        if hasattr(cls, 'objects'):
            today = datetime.date.today()
            q_end_missing = Q(end_date=None)
            q_end_not_passed = Q(end_date__gte=today)
            q = Q(
                q_end_missing
                | q_end_not_passed
            )
            return cls.objects.all().filter(start_date__lte=today).filter(q)
        else:
            raise AttributeError('Class does not have attribute \'objects\'')

    @classmethod
    def all_filter_has_been_active(cls):
        """
        Return a query set of objects filtering only the has-been-active ones
        :return: a query set of has-been-active objects
        """

        if hasattr(cls, 'objects'):
            today = datetime.date.today()
            return cls.objects.all().filter(end_date_lt=today)
        else:
            raise AttributeError('Class does not have attribute \'objects\'')

    @property
    def is_active(self):
        """
        Return whether the entity is currently active
        :return: True if start date has passed and end date has not
        """

        today = datetime.date.today()
        if self.end_date is not None:
            return self.start_date <= today <= self.end_date
        else:
            return self.start_date <= today

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
