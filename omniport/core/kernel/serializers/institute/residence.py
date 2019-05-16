import swapper

from formula_one.serializers.base import ModelSerializer


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
