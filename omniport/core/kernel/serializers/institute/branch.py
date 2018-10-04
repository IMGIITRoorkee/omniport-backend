import swapper

from kernel.serializers.root import ModelSerializer
from kernel.serializers.institute.department import DepartmentSerializer

class BranchSerializer(ModelSerializer):
    """
    Serializer for Branch
    """

    department = DepartmentSerializer(
        read_only=True,
    )

    class Meta:
        """
        Meta class for Branch
        """

        model = swapper.load_model('kernel', 'Branch')
        fields = (
            'id',
            'code',
            'name',
            'degree',
            'department',
        )

