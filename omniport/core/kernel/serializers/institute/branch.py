import swapper

from formula_one.serializers.base import ModelSerializer
from omniport.utils import switcher

DegreeSerializer = switcher.load_serializer('kernel', 'Degree')
DepartmentSerializer = switcher.load_serializer('kernel', 'Department')


class BranchSerializer(ModelSerializer):
    """
    Serializer for Branch objects
    """

    degree = DegreeSerializer(
        read_only=True,
    )
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
