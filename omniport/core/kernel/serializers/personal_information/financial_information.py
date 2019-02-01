import swapper

from kernel.serializers.root import ModelSerializer

FinancialInformation = swapper.load_model('kernel', 'FinancialInformation')


class FinancialInformationSerializer(ModelSerializer):
    """
    Serializer for FinancialInformation objects
    """

    class Meta:
        """
        Meta class for FinancialInformationSerializer
        """

        model = FinancialInformation
        exclude = [
            'person',
            'id',
            'datetime_created',
            'datetime_modified',
        ]
