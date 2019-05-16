import swapper

from formula_one.serializers.base import ModelSerializer
from kernel.serializers.institute.department import DepartmentSerializer
from kernel.serializers.person import AvatarSerializer


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

        fields = [
            'id',
            'person',
            'department',
            'designation',
        ]
