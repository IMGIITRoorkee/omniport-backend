import swapper

from kernel.serializers.root import ModelSerializer
from kernel.serializers.institute.department import DepartmentSerializer

class ContactInformationSerializer(ModelSerializer):
    """
    Serializer for Contact information
    """

    class Meta:
        """
        Meta class for Contact information
        """

        model = swapper.load_model('kernel', 'ContactInformation')
        fields = (
            'primary_phone_number',
            'secondary_phone_number',
            'email_address',
            'institute_webmail_address',
        )

