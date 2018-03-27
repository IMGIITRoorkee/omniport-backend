from django.db import models
from django_permanent import models as permanent_models


class Model(permanent_models.PermanentModel):
    """
    This abstract root model should be inherited by all model classes
    Do not inherit from django.db.models.Model!
    """

    datetime_created = models.DateTimeField(auto_now_add=True)
    datetime_modified = models.DateTimeField(auto_now=True)

    class Meta:
        """
        Meta class for Model
        """

        abstract = True
