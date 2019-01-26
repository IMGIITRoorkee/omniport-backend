from rest_framework import serializers

from base_auth.managers.get_user import get_user
from base_auth.models import User


class RetrieveUserSerializer(serializers.Serializer):
    """
    Stores an instance of User with the given username
    """

    user = None
    username = serializers.CharField()

    def validate_username(self, username):
        """
        Validates the username by seeing if any User object matches it
        :param username: the username whose existence is being checked
        :return: the username after validation
        :raise serializers.ValidationError: if no user has the given username
        """

        try:
            user = get_user(username=username)
            self.user = user
        except User.DoesNotExist:
            raise serializers.ValidationError('Username does not exist.')

        return username
