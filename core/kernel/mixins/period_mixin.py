import datetime
from enum import auto, Flag

from django.db import models
from django.db.models import Q, Model


class ActiveStatus(Flag):
    """
    These flags describe whether the
    """

    # Base flags
    HAS_BEEN_ACTIVE = auto()
    IS_ACTIVE = auto()
    WILL_BE_ACTIVE = auto()

    # Aliases
    IS_INACTIVE = ~IS_ACTIVE
    ANY = HAS_BEEN_ACTIVE | IS_ACTIVE | WILL_BE_ACTIVE
    NONE = 0


class PeriodMixin(Model):
    """
    This mixin adds information about the start and end of any entity's
    active period
    """

    start_date = models.DateField()
    # A blank end date denotes that the end date is not known and in the future
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
    def objects_filter(cls, active_status):
        """
        Return a query set of objects that match the specified active status
        :param active_status: the active status of objects to keep in the set
        :return: a query set of objects with the specified active status
        """

        if hasattr(cls, 'objects'):
            today = datetime.date.today()

            if ActiveStatus.HAS_BEEN_ACTIVE in active_status:
                q_has_been_active = Q(end_date__lt=today)
            else:
                q_has_been_active = Q()

            if ActiveStatus.IS_ACTIVE in active_status:
                q_start = Q(start_date__lte=today)
                q_end_missing = Q(end_date=None)
                q_end_not_passed = Q(end_date__gte=today)
                q_end = Q(q_end_missing | q_end_not_passed)
                q_is_active = Q(q_start & q_end)
            else:
                q_is_active = Q()

            if ActiveStatus.WILL_BE_ACTIVE in active_status:
                q_will_be_active = Q(start_date__gt=today)
            else:
                q_will_be_active = Q()

            q = q_has_been_active | q_is_active | q_will_be_active
            return cls.objects.filter(q)
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
    def active_status(self):
        """
        Return a flag from ActiveStatus denoting the instance's active status
        :return: a flag from ActiveStatus denoting the instance's active status
        """

        if self.is_active:
            return ActiveStatus.IS_ACTIVE
        elif self.has_already_ended:
            return ActiveStatus.HAS_BEEN_ACTIVE
        elif self.is_yet_to_begin:
            return ActiveStatus.WILL_BE_ACTIVE

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
