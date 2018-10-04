import swapper

from kernel.serializers.root import ModelSerializer
from kernel.serializers.person import AvatarSerializer
from kernel.serializers.institute.department import DepartmentSerializer


class FacultyMemberSerializer(ModelSerializer):
    """
    Serializer for FacultyMember objects
    """

    person = AvatarSerializer(
        read_only=True,
    )
    department = DepartmentSerializer(
        read_only=True,
    )

    class Meta:
        """
        Meta class for FacultyMemberSerializer
        """

        model = swapper.load_model('kernel', 'FacultyMember')
        fields = (
            'person',
            'department',
            'designation',
        )
