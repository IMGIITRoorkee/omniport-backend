import swapper

from kernel.serializers.root import ModelSerializer


class ResidenceSerializer(ModelSerializer):
    """
    Serializer for Residence objects
    """

    class Meta:
        """
        Meta class for Residence
        """

        model = swapper.load_model('kernel', 'Residence')
        fields = [
            'id',
            'code',
            'name',
        ]
