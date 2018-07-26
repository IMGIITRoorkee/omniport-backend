import swapper

from kernel.serializers.root import ModelSerializer


class PersonSerializer(ModelSerializer):
    """
    Serializer for Person objects
    """

    class Meta:
        """
        Meta class for PersonSerializer
        """

        model = swapper.load_model('kernel', 'Person')
        fields = '__all__'
