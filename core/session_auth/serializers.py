from django.contrib.auth import authenticate
from rest_framework import serializers
from rest_framework_simplejwt.serializers import PasswordField


class LoginSerializer(serializers.Serializer):
    """
    Stores the username and password for logging a user in
    """

    user = None
    username = serializers.CharField()
    password = PasswordField()

    def validate(self, data):
        """
        Authenticate the username and password to see if they are valid
        :param data: the data to check for validity
        :return: the data if it is valid
        :raise ValidationError: if the username and password do not match
        """

        request = self.context.get('request')

        user = authenticate(
            request,
            username=data.get('username'),
            password=data.get('password')
        )
        if user is not None:
            self.user = user
        else:
            raise serializers.ValidationError('Invalid credentials provided')

        return data
