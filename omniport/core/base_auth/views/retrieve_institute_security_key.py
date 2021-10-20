import logging

from rest_framework import status, generics, response

from base_auth.managers.get_user import get_user
from token_auth.authentication import AppAccessTokenAuthentication
from token_auth.permission.app_access_token import TokenHasPermissionKey

logger = logging.getLogger('core')

class RetrieveInstituteSecurityKey(generics.GenericAPIView):
    """
    This view, when responding to a GET request, takes the
    username, and return its institute security key
    """

    permission_key = 'retrieve-isk'
    authentication_classes = [AppAccessTokenAuthentication]
    permission_classes = [TokenHasPermissionKey]

    def get(self, request):
        """
        View to serve GET requests
        :param request: the request that is to be responded to
        :return: the response for request
        """

        app_name = request.user.app_name
        username = request.GET.get('username')
        
        logger.info(f'{app_name}: requested for the isk of username: {username}')

        response_data = dict()

        if username:
            try:
                user = get_user(username=username)
                response_data['username'] = user.username
                response_data['institute_security_key'] = user.institute_security_key
                response_status = status.HTTP_200_OK
                logger.info(f'{app_name}: retrieved the isk for username: {username}')
            except Exception:
                response_data['error'] = 'Invalid username'
                response_status = status.HTTP_404_NOT_FOUND
                logger.info(f'{app_name}: Invalid username: {username}')
        else:
            response_data['error'] = 'username not provided'
            response_status = status.HTTP_400_BAD_REQUEST

        return response.Response(
            data=response_data,
            status=response_status
        )
