import swapper

from kernel.models.roles.base import AbstractRole

class Guest(AbstractRole):
    """
    This class implements Guest Role
    """

    class Meta:
        """
        Meta class for Guest
        """

        swappable = swapper.swappable_setting('kernel', 'Guest')
