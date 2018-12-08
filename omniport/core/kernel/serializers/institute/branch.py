import swapper

from kernel.serializers.institute.department import DepartmentSerializer
from kernel.serializers.root import ModelSerializer


class BranchSerializer(ModelSerializer):
    """
    Serializer for Branch objects
    """

    department = DepartmentSerializer(
        read_only=True,
    )

    class Meta:
        """
        Meta class for BranchSerializer
        """

        model = swapper.load_model('kernel', 'Branch')

        fields = [
            'id',
            'code',
            'name',
            'degree',
            'department',
        ]
