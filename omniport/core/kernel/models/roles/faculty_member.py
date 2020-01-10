import swapper
from django.db import models
from django.contrib.contenttypes import fields as contenttypes_fields
from django.contrib.contenttypes import models as contenttypes_models

from kernel.models.roles.base import AbstractRole


class AbstractFacultyMember(AbstractRole):
    """
    This model holds information pertaining to a faculty member
    """

    # Relationship with the department or center entity
    _limits = models.Q(
        app_label=swapper.get_model_name('kernel', 'Department').split('.')[0],
        model='department',
    ) | models.Q(
        app_label=swapper.get_model_name('kernel', 'Centre').split('.')[0],
        model='centre',
    )
    entity_content_type = models.ForeignKey(
        to=contenttypes_models.ContentType,
        on_delete=models.CASCADE,
        limit_choices_to=_limits,
    )
    entity_object_id = models.BigIntegerField()
    content_object = contenttypes_fields.GenericForeignKey(
        ct_field='entity_content_type',
        fk_field='entity_object_id',
    )

    designation = models.CharField(
        max_length=63,
    )

    class Meta:
        """
        Meta class for AbstractFacultyMember
        """

        abstract = True

    def __str__(self):
        """
        Return the string representation of the model
        :return: the string representation of the model
        """

        person = self.person
        designation = self.designation
        department = self.department
        return f'{person} - {designation}, {department}'

    @property
    def is_retired(self):
        """
        Return whether or not the faculty member is retired
        :return: True if the role period has already ended, False otherwise
        """

        return self.has_already_ended

    @property
    def department(self):
        """
        Return the department of the branch
        :return: the department object
        """

        if self.entity_content_type.name == 'centre':
            Class = swapper.load_model('shell', 'Centre')
        else:
            Class = swapper.load_model('shell', 'Department')

        department = Class.objects.get(id=self.entity_object_id)

        return department


class FacultyMember(AbstractFacultyMember):
    """
    This class implements AbstractFacultyMember
    """

    class Meta:
        """
        Meta class for FacultyMember
        """

        swappable = swapper.swappable_setting('kernel', 'FacultyMember')
