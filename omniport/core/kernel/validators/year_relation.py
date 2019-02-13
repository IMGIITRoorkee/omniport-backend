import datetime

from django.core.exceptions import ValidationError
from django.utils.deconstruct import deconstructible


@deconstructible
class YearRelationValidator:
    """
    This validator checks if the given year lies in an acceptable period of time
    relative to the present
    """

    def __init__(self, time_relation='=='):
        """
        Initialise a callable instance of the class with the given parameters
        :param time_relation: the relation of the year submitted relative to now
        """

        self.time_relation = time_relation

    def check(self, value):
        """
        Check if the value meets all required criteria
        :param value: the value of the field
        :return: True if the value meets the criteria, False otherwise
        """

        current_year = datetime.date.today().year

        if self.time_relation == '<':
            return value < current_year
        elif self.time_relation == '<=':
            return value <= current_year
        elif self.time_relation == '>':
            return value > current_year
        elif self.time_relation == '>=':
            return value >= current_year
        else:  # self.time_relation == '=='
            return value == current_year

    def __call__(self, value):
        """
        Call the check() function and raise an error if validation fails
        :param value: the value of the field being validated
        :raise: ValidationError, if the year is in the wrong period of time
        """

        if not self.check(value):
            raise ValidationError(
                'The year is in the wrong period of time. '
                f'The year should be {self.time_relation} current year.'
            )
