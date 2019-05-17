import swapper

from kernel.serializers.roles.base import RoleSerializer
from omniport.utils import switcher

DepartmentSerializer = switcher.load_serializer('kernel', 'Department')


class FacultyMemberSerializer(RoleSerializer):
    """
    Serializer for FacultyMember objects
    """

    department = DepartmentSerializer(
        read_only=True,
    )

    class Meta:
        """
        Meta class for FacultyMemberSerializer
        """

        model = swapper.load_model('kernel', 'FacultyMember')

        fields = [
            'id',
            'person',
            'department',
            'designation',
        ]
