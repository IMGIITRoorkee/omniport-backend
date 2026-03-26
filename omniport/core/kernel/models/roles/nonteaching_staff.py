import swapper
from kernel.models.roles.base import AbstractRole

class AbstractNonTeachingStaff(AbstractRole):
    """
    This model holds information pertaining to a non-teaching staff member
    """

    class Meta:
        """
        Meta class for AbstractNonTeachingStaff
        """

        abstract = True
    
    def __str__(self):
        """
        Return the string representation of the model
        :return: the string representation of the model
        """

        person = self.person
        return f'{person}'

class NonTeachingStaff(AbstractNonTeachingStaff):
    """
    This class implements NonTeachingStaff Role
    """

    class Meta:
        """
        Meta class for NonTeachingStaff
        """

        swappable = swapper.swappable_setting('kernel', 'NonTeachingStaff')
