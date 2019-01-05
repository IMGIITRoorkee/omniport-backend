from kernel.models import ContactInformation
from kernel.serializers.root import ModelSerializer


class ContactInformationSerializer(ModelSerializer):
    """
    Serializer for ContactInformation objects
    """

    class Meta:
        """
        Meta class for ContactInformationSerializer
        """

        model = ContactInformation

        exclude = [
            'datetime_created',
            'datetime_modified',
            'entity_content_type',
            'entity_object_id',
        ]
        read_only_fields = [
            'email_address_verified',
            'institute_webmail_address',
        ]

    def update(self, instance, validated_data):
        """

        :param instance:
        :param validated_data:
        :return:
        """

        original_email_address = instance.email_address
        new_email_address = validated_data.get('email_address')

        instance = super().update(instance, validated_data)

        if original_email_address != new_email_address:
            instance.email_address_verified = False
            instance.save()

        return instance
