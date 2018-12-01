from django.db import models


class Model(models.Model):
    """
    This abstract root model should be inherited by all model classes
    Provides additional features like soft delete and datetime information
    Do not inherit from django.db.models.Model!
    """

    datetime_created = models.DateTimeField(auto_now_add=True)
    datetime_modified = models.DateTimeField(auto_now=True)

    class Meta:
        """
        Meta class for Model
        """

        abstract = True
