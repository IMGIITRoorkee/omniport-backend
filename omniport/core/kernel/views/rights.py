from rest_framework import status, generics, permissions, response

from kernel.utils import rights


class Rights(generics.GenericAPIView):
    """
    This view shows if the current user has the given rights
    """

    permission_classes = [permissions.IsAuthenticated, ]

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
            response_data = {
                'hasRights': has_rights,
            }
            return response.Response(
                data=response_data,
                status=status.HTTP_200_OK
            )
        except AttributeError:
            response_data = {
                'errors': {
                    "which": [
                        "Non-existent right",
                    ],
                },
            }
            return response.Response(
                data=response_data,
                status=status.HTTP_400_BAD_REQUEST
            )
