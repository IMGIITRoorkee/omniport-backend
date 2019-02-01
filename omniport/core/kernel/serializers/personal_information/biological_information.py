import swapper

from kernel.serializers.root import ModelSerializer

BiologicalInformation = swapper.load_model('kernel', 'BiologicalInformation')


class BiologicalInformationSerializer(ModelSerializer):
    """
    Serializer for BiologicalInformation objects
    """

    class Meta:
        """
        Meta class for BiologicalInformationSerializer
        """

        model = BiologicalInformation
        exclude = [
            'person',
            'id',
            'datetime_created',
            'datetime_modified',
        ]
        read_only_fields = [
            'date_of_birth',
        ]
