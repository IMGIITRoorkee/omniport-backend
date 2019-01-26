from rest_framework import serializers

from base_auth.serializers.retrieve_user import RetrieveUserSerializer


class ResetPasswordSerializer(RetrieveUserSerializer):
    """
    Stores the secret answer and the new password for changing it
    """

    secret_answer = serializers.CharField()
    new_password = serializers.CharField()

    def validate_secret_answer(self, secret_answer):
        """
        Validate the secret answer by comparing it with the stored answer
        :param secret_answer: the secret answer to check for correctness
        :return: the secret answer if it is correct
        :raise serializers.ValidationError: if the secret answer is wrong
        """

        if self.user.failed_reset_attempts >= 3:
            raise serializers.ValidationError('Reset attempts exceeded limit.')

        if not self.user.check_secret_answer(secret_answer):
            user = self.user
            user.failed_reset_attempts = user.failed_reset_attempts + 1
            user.save()
            raise serializers.ValidationError(
                'Incorrect credentials. '
                f'Attempts left: {3 - user.failed_reset_attempts}'
            )

        return secret_answer
