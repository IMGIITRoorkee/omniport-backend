from formula_one.serializers.base import ModelSerializer
from omniport.utils import switcher

AvatarSerializer = switcher.load_serializer('kernel', 'Person', 'Avatar')


class RoleSerializer(ModelSerializer):
    """
    Serializer for Role objects
    """

    person = AvatarSerializer(
        read_only=True,
    )
