import swapper

from kernel.serializers.root import ModelSerializer
from kernel.serializers.person import AvatarSerializer
from kernel.serializers.institute.branch import BranchSerializer
from kernel.managers.get_role import get_all_roles


class StudentSerializer(ModelSerializer):
    """
    Serializer for Student objects
    """

    person = AvatarSerializer(
        read_only=True,
    )
    branch = BranchSerializer(
        read_only=True,
    )

    class Meta:
        """
        Meta class for StudentSerializer
        """

        model = swapper.load_model('kernel', 'Student')
        fields = (
            'person',
            'branch',
            'current_year',
            'current_semester',
        )
