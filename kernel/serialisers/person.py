import swapper

from kernel.serialisers.root import ModelSerialiser


class PersonSerialiser(ModelSerialiser):
    """
    Serialiser for Person objects
    """

    class Meta:
        """
        Meta class for PersonSerialiser
        """

        model = swapper.load_model('kernel', 'Person')
        fields = '__all__'
