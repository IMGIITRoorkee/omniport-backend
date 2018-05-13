from django.contrib.auth import authenticate
from rest_framework import serializers
from rest_framework_simplejwt.serializers import PasswordField


class LoginSerializer(serializers.Serializer):
    """

    """

    user = None
    username = serializers.CharField(max_length=63)
    password = PasswordField()

    def validate(self, data):
        """
        Authenticate the username and password
        :param data:
        :return:
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
