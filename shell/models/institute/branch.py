from django.db import models

from kernel.models import AbstractBranch
from shell.constants import (
    UNDERGRADUATE_DEGREES,
    POSTGRADUATE_DEGREES,
    DOCTORATE_DEGREES,
    DEGREES,
    GRADUATIONS,
)


class Branch(AbstractBranch):
    """
    Make changes to AbstractBranch to suit IIT Roorkee
    """

    degree = models.CharField(
        max_length=7,
        unique=True,
        choices=DEGREES,
    )

    class Meta:
        """
        Meta class for Branch
        """

        verbose_name_plural = 'branches'

    @property
    def graduation(self):
        """
        Return the type of graduation of the course
        :return: the type of graduation of the course
        """

        undergraduate_degree_codes = [
            code
            for (code, verbose) in UNDERGRADUATE_DEGREES
        ]
        if self.degree in undergraduate_degree_codes:
            return GRADUATIONS[0]

        postgraduate_degree_codes = [
            code
            for (code, verbose) in POSTGRADUATE_DEGREES
        ]
        if self.degree in postgraduate_degree_codes:
            return GRADUATIONS[1]

        doctorate_degree_codes = [
            code
            for (code, verbose) in DOCTORATE_DEGREES
        ]
        if self.degree in doctorate_degree_codes:
            return GRADUATIONS[2]
