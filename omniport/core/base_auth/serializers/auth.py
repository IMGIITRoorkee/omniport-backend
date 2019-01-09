import random
import string

from rest_framework import serializers
from rest_framework_simplejwt.serializers import PasswordField

from base_auth.managers.get_user import get_user
from base_auth.models import User


class UserRetrievalSerializer(serializers.Serializer):
    """
    Stores an instance of User with the given username
    """

    user = None
    username = serializers.CharField()

    def validate_username(self, username):
        """
        Validates the username by seeing if any User object matches
        :param username: the username whose existence is being checked
        :return: the username after validation
        :raise ValidationError: if no user has the given username
        """

        try:
            user = get_user(username=username)
            self.user = user
        except User.DoesNotExist:
            raise serializers.ValidationError('Non-existent username')

        return username


class ChangePasswordSerializer(serializers.Serializer):
    """
    Stores the old and the new password for a user intending to change it
    """

    old_password = PasswordField()
    new_password = PasswordField()

    def validate_old_password(self, old_password):
        """
        Validates the old password by checking if it authenticates the user
        :param old_password: the old password for a user
        :return: the old password if it authenticates the user
        :raise ValidationError: if the old password is incorrect
        """

        user = self.context.get('request').user

        if not user.check_password(old_password):
            raise serializers.ValidationError('Incorrect old password')

        return old_password


class ResetPasswordSerializer(UserRetrievalSerializer):
    """
    Stores the secret answer and the new password for changing it
    """

    secret_answer = serializers.CharField()
    new_password = PasswordField()

    def validate_secret_answer(self, secret_answer):
        """
        Validate the secret answer by comparing it with the stored answer
        :param secret_answer: the secret answer to check for correctness
        :return: the secret answer if it is correct
        :raise ValidationError: if the secret answer is wrong
        """

        if self.user.failed_reset_attempts >= 3:
            raise serializers.ValidationError('Reset attempts exceeded limit')

        if not self.user.check_secret_answer(secret_answer):
            user = self.user
            user.failed_reset_attempts = user.failed_reset_attempts + 1
            user.save()
            raise serializers.ValidationError('Incorrect credentials')

        return secret_answer

    def validate(self, data):
        """
        Check if the user in question has reset attempts left
        :param data: the data to check for validity
        :return: the data if the user has not exceeded failed attempts
        :raise ValidationError: if the user has failed to reset password thrice
        """

        if self.user.failed_reset_attempts >= 3:
            print(self.user.failed_reset_attempts)
            raise serializers.ValidationError('Reset attempts exceeded limit')

        return data


class LockpickingSerializer(UserRetrievalSerializer):
    """
    Stores the new password if it is being reset by a maintainer
    """

    new_password = PasswordField(required=False)

    def validate(self, data):
        """
        Generate a random password in case one is not provided
        :param data: the data to check for validity
        :return: the data
        """

        new_password = data.get('new_password', None)
        if not new_password:
            allowed_chars = string.ascii_uppercase + string.digits
            password_length = 8
            new_password = ''.join(
                random.SystemRandom().choice(allowed_chars)
                for _ in range(password_length)
            )
            data['new_password'] = new_password

        return data
