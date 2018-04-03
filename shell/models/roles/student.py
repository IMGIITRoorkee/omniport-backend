from django.core.validators import RegexValidator
from django.db import models

from kernel.models import AbstractStudent


class Student(AbstractStudent):
    """
    Make changes to AbstractStudent to suit IIT Roorkee
    """

    enrolment_number = models.CharField(
        max_length=8,
        validators=[
            RegexValidator(r'\d{8}'),
        ],
        primary_key=True,
        unique=True,
    )
