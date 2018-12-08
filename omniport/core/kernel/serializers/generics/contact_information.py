import swapper

from kernel.serializers.root import ModelSerializer


class ContactInformationSerializer(ModelSerializer):
    """
    Serializer for ContactInformation objects
    """

    class Meta:
        """
        Meta class for ContactInformationSerializer
        """

        model = swapper.load_model('kernel', 'ContactInformation')

        fields = [
            'primary_phone_number',
            'secondary_phone_number',
            'email_address',
            'email_address_verified',
            'institute_webmail_address',
            'video_conference_id',
        ]
