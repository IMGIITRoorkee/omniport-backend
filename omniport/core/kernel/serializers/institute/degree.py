import swapper
from rest_framework import serializers

from kernel.serializers.root import ModelSerializer


class DegreeSerializer(ModelSerializer):
    """
    Serializer for Branch objects
    """

    graduation = serializers.SerializerMethodField(
        read_only=True,
    )

    def get_graduation(self, instance):
        """
        Return the graduation level of the degree, which is the first element
        of the graduation tuple
        :return: the first element of the graduation tuple
        """

        return instance.graduation[1]

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
