import swapper

from kernel.serializers.root import ModelSerializer


class DepartmentSerializer(ModelSerializer):
    """
    Serializer for Departments objects
    """

    class Meta:
        """
        Meta class for DepartmentSerializer
        """

        model = swapper.load_model('kernel', 'Department')
        fields = (
            'id',
            'code',
            'name',
        )
