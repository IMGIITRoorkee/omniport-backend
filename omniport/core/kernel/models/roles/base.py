import swapper
from django.db import models

from formula_one.mixins.period_mixin import PeriodMixin
from formula_one.models.base import Model


class AbstractRole(PeriodMixin, Model):
    """
    This model holds information pertaining to a role held by a person
    """

    person = models.OneToOneField(
        to=swapper.get_model_name('kernel', 'Person'),
        on_delete=models.CASCADE,
    )

    class Meta:
        """
        Meta class for AbstractRole
        """

        abstract = True
