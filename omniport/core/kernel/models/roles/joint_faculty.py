from tabnanny import verbose
import swapper
from django.db import models
from django.contrib.contenttypes import fields as contenttypes_fields
from django.contrib.contenttypes import models as contenttypes_models

from formula_one.models.base import Model
from kernel.models.roles.base import AbstractRole


class AbstractJointFacultyMembership(Model):
    """
    This model holds information pretaining to department/centre and
    designation of joint faculty members.
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
        Meta class for AbstractJointFacultyMembership
        """

        abstract = True
        constraints = [
            models.UniqueConstraint(
                fields=[
                    'entity_content_type',
                    'entity_object_id',
                    'designation',
                ],
                name='unique_designation',
            ),
        ]

    def __str__(self):
        """
        Return the string representation of the model
        :return: the string representation of the model
        """

        designation = self.designation
        department = self.department
        return f'{designation}, {department}'


    @property
    def department(self):
        """
        Return the department/centre of the joint faculty
        :return: the department/centre object
        """

        if self.entity_content_type.name == 'centre':
            Class = swapper.load_model('shell', 'Centre')
        else:
            Class = swapper.load_model('shell', 'Department')

        department = Class.objects.get(id=self.entity_object_id)

        return department


class JointFacultyMembership(AbstractJointFacultyMembership):
    """
    This class implements AbstractJointFacultyMembership
    """

    class Meta:
        """
        Meta class for JointFacultyMembership
        """

        swappable = swapper.swappable_setting('kernel', 'JointFacultyMembership')


class AbstractJointFaculty(AbstractRole):
    """
    This model holds information pertaining to a joint faculty member
    """

    memberships = models.ManyToManyField(
        to=swapper.get_model_name('kernel', 'JointFacultyMembership'),
        related_name='joint_faculty_members'
    )

    class Meta:
        """
        Meta class for AbstractJointFaculty
        """

        abstract = True
        verbose_name_plural = 'Joint Faculties'
    
    def __str__(self):
        """
        Return the string representation of the model
        :return: the string representation of the model
        """
        person = self.person
        departments = self.departments

        return f'{person} - Joint Faculty, {departments}'

    @property
    def departments(self):
        """
        Return the list of departments/centres of the joint faculty
        :return: the departments/centres list
        """
        departments = list()
        for membership in self.memberships.all():
            if membership.entity_content_type.name == 'centre':
                Class = swapper.load_model('shell', 'Centre')
            else:
                Class = swapper.load_model('shell', 'Department')

            departments.append(Class.objects.get(id=membership.entity_object_id))

        return departments


class JointFaculty(AbstractJointFaculty):
    """
    This class implements AbstractJointFaculty
    """

    class Meta:
        """
        Meta class for JointFaculty
        """

        swappable = swapper.swappable_setting('kernel', 'JointFaculty')
