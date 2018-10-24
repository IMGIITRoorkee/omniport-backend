from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from kernel.utils import rights


class Rights(GenericAPIView):
    """
    This view shows some personal information of the currently logged in user
    """

    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        """
        View to serve GET requests
        :param request: the request that is to be responded to
        :param args: arguments
        :param kwargs: keyword arguments
        :return: the response for request
        """

        which = request.query_params.get('which')
        user = request.user
        try:
            rights_function = getattr(rights, f'has_{which}_rights')
            has_rights = rights_function(user)
        except AttributeError:
            has_rights = False
        response = {
            'hasRights': has_rights,
        }
        return Response(response)
