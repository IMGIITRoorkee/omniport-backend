from django.db import models

from kernel.models import AbstractFacultyMember
from shell.constants import FACULTY_DESIGNATIONS


class FacultyMember(AbstractFacultyMember):
    """
    Make changes to AbstractFacultyMember to suit IIT Roorkee
    """

    designation = models.CharField(
        max_length=3,
        choices=FACULTY_DESIGNATIONS,
    )

    def __str__(self):
        """
        Return the string representation of the model
        :return: the string representation of the model
        """

        person = self.person
        designation = self.get_designation_display()
        department = self.department
        return f'{person} - {designation}, {department}'
