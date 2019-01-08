from rest_framework import viewsets, mixins, permissions

from open_auth.models import Application
from open_auth.serializers.application import ApplicationAuthoriseSerializer


class ApplicationViewSet(
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet,
):
    """
    Viewset for R operations on Application
    """

    permission_classes = [permissions.IsAuthenticated, ]
    serializer_class = ApplicationAuthoriseSerializer
    queryset = Application.objects.filter(is_approved=True)
    lookup_field = 'client_id'
    pagination_class = None
