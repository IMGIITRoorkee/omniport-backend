from django.contrib.auth import models as auth_models
from django.contrib.auth.hashers import make_password, check_password
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from kernel.managers import auth
from kernel.utils.rights import has_omnipotence_rights


class User(auth_models.PermissionsMixin, auth_models.AbstractBaseUser):
    """
    This model holds the authentication information of a person
    """

    person = models.OneToOneField(
        to='Person',
        blank=True,
        null=True,
        on_delete=models.CASCADE,
    )

    # This is an alternate username for logging in
    # This field is completely optional and makes for a fun easter egg
    # Set it to anything you like from the administrative interface
    # For example, you may have 'me_me_big_boy' as your username
    username = models.CharField(
        max_length=15,
        blank=True,
        null=True,
        default=None,
        unique=True,
    )

    secret_question = models.CharField(
        max_length=127,
        blank=True,
    )
    secret_answer = models.CharField(
        max_length=2047,
        blank=True,
    )
    failed_reset_attempts = models.IntegerField(
        validators=[
            MaxValueValidator(3),
            MinValueValidator(0),
        ],
        default=0,
    )

    objects = auth.UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

    def set_secret_answer(self, given_answer):
        """
        Set the given answer as the new security answer
        :param given_answer: the new answer to store in the database
        """

        encoded_answer = make_password(
            password=given_answer,
        )
        self.secret_answer = encoded_answer
        self.save()

    def check_secret_answer(self, given_answer):
        """
        Compare the given answer with the set security answer
        :param given_answer: the answer to check against the database
        :return: true if the answers match, false otherwise
        """

        return check_password(
            password=given_answer,
            encoded=self.secret_answer,
        )

    def has_perm(self, perm, obj=None):
        """
        Add an alternative check to the default check for permissions
        :param perm: the permission to check for
        :param obj: the object on which to check permissions instead of self
        :return: True if the user is an administrative IMGian, false otherwise
        """

        has_permission = super(User, self).has_perm(perm, obj)
        return has_omnipotence_rights(self) or has_permission

    def has_perms(self, perm_list, obj=None):
        """
        Add an alternative check to the default check for permissions
        :param perm_list: the list of permissions to check for
        :param obj: the object on which to check permissions instead of self
        :return: True if the user is an administrative IMGian, false otherwise
        """

        has_permissions = super(User, self).has_perms(perm_list, obj)
        return has_omnipotence_rights(self) or has_permissions

    def get_short_name(self):
        """
        Return the short name of the associated person
        :return: the short name of the associated person, or id if none found
        """

        try:
            return self.person.get_short_name()
        except AttributeError:
            return str(self.id)

    def get_full_name(self):
        """
        Return the full name of the associated person
        :return: the full name of the associated person, or id if none found
        """

        try:
            return self.person.get_full_name()
        except AttributeError:
            return str(self.id)

    def __str__(self):
        """
        Return the string representation of the model
        :return: the string representation of the model
        """

        return self.get_full_name()
