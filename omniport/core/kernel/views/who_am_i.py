import logging
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from omniport.utils import switcher

logger = logging.getLogger('security')
AvatarSerializer = switcher.load_serializer('kernel', 'Person', 'Avatar')


class WhoAmI(GenericAPIView):
    """
    This view shows personal information of the currently logged in user.
    """

    permission_classes = [IsAuthenticated, ]
    serializer_class = AvatarSerializer

    def get(self, request, *args, **kwargs):
        """
        View to serve GET requests.
        Returns user profile for display purposes only.
        Role/permissions determined server-side, never in response.

        :param request: the request that is to be responded to
        :param args: arguments
        :param kwargs: keyword arguments
        :return: the response for request
        """
        try:
            person = request.person
            serializer = self.get_serializer_class()(person)
            data = serializer.data

            # Security: Remove any authorization-related fields that might be present
            sensitive_fields = ['role', 'is_admin', 'permissions', 'groups', 'is_staff', 'is_superuser']
            for field in sensitive_fields:
                data.pop(field, None)

            return Response(data, status=status.HTTP_200_OK)
        except Exception as e:
            logger.error(f"Error in WhoAmI endpoint: {e}")
            return Response(
                {'error': 'Could not fetch user information'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
