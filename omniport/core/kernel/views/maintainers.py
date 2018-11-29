import swapper
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from kernel.permissions.has_role import get_has_role
from kernel.serializers.roles.maintainers import MaintainerSerializer

Maintainer = swapper.load_model('kernel', 'Maintainer')


class MaintainerViewSet(ModelViewSet):
    """
    The view for CRUD operations of maintainers
    """

    permission_classes = [
        IsAuthenticated,
        get_has_role('Maintainer'),
    ]

    http_method_names = [
        'get',
    ]

    serializer_class = MaintainerSerializer

    queryset = Maintainer.objects.all()

    pagination_class = None
