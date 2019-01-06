import swapper

from kernel.serializers.root import ModelSerializer


class DegreeSerializer(ModelSerializer):
    """
    Serializer for Branch objects
    """

    class Meta:
        """
        Meta class for DegreeSerializer
        """

        model = swapper.load_model('kernel', 'Degree')

        fields = [
            'id',
            'code',
            'name',
            'graduation',
        ]
