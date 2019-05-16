import swapper
from django.db import models

from kernel.models.roles.base import AbstractRole


class AbstractMaintainer(AbstractRole):
    """
    This model holds information pertaining to a maintainer
    """

    """
    Indicates the maintainer's role within the organisation.
    Here it is used to identify the core duty of the maintainer.
    
    Example: developer, designer
    """
    role = models.CharField(
        max_length=127,
        blank=True,
    )

    """
    Indicates the maintainer's hierarchical level in the organization.
    This field rises as the maintainer moves up in the hierarchy.
    
    Example: webmaster, hub-coordinator, project leader, coordinator
    """
    designation = models.CharField(
        max_length=127,
        blank=True,
    )

    """
    This is a floating field in case the upper two are not enough or flexible.
    Here it is used to assign duties to each maintainer.
    
    Example: chief technology coordinator, chief security coordinator
    """
    post = models.CharField(
        max_length=127,
        blank=True,
    )

    class Meta:
        """
        Meta class for AbstractMaintainer
        """

        abstract = True

    def __str__(self):
        """
        Return the string representation of the model
        :return: the string representation of the model
        """

        person = self.person
        role = self.role
        designation = self.designation
        post = self.post
        return f'{person} - {role}, {designation} ({post})'


class Maintainer(AbstractMaintainer):
    """
    This class implements AbstractMaintainer
    """

    class Meta:
        """
        Meta class for Maintainer
        """

        swappable = swapper.swappable_setting('kernel', 'Maintainer')
