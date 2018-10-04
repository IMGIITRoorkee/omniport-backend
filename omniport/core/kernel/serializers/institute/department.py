import swapper

from kernel.serializers.root import ModelSerializer


class DepartmentSerializer(ModelSerializer):
    """
    Serializer for Departments in Institute
    """

    class Meta:
        """
        Meta class for Depratmnts
        """

        model = swapper.load_model('kernel', 'Department')
        fields = (
            'id',
            'code',
            'name',
        )

