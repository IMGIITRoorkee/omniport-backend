import swapper

from kernel.serializers.institute.department import DepartmentSerializer
from kernel.serializers.roles.base import RoleSerializer


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
