import logging

from rest_framework import status, generics, response

from base_auth.managers.get_user import get_user
from token_auth.authentication import AppAccessTokenAuthentication
from token_auth.permission.app_access_token import TokenHasPermissionKey

logger = logging.getLogger('core')

class VerifyInstituteSecurityKey(generics.GenericAPIView):
    """
    This view, when responding to a GET request, takes the
    username, the institute_security_key and verify if the credentials are valid
    """

    permission_key = 'verify-isk'
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
        institute_security_key = request.GET.get('isk')
        
        logger.info(f'{app_name}: requested to verify isk for username: {username}')

        response_data = {
            'valid': False,
        }
        response_status = status.HTTP_401_UNAUTHORIZED

        if username and institute_security_key:
            try:
                user = get_user(username=username)
                if user.institute_security_key == institute_security_key:
                    response_data['valid'] = True
                    response_status = status.HTTP_200_OK
                    logger.info(f'{app_name}: successfully verified the security key for username: {username}')
                else:
                    response_data['error'] = 'Invalid institute security key'
                    response_status = status.HTTP_401_UNAUTHORIZED
                    logger.info(f'{app_name}: Invalid security key for username: {username}')
            except Exception:
                response_data['error'] = 'Invalid username'
                response_status = status.HTTP_404_NOT_FOUND
                logger.info(f'{app_name}: Invalid username: {username}')
        else:
            response_data['error'] = 'username and institute_security_key not provided'
            response_status = status.HTTP_400_BAD_REQUEST

        return response.Response(
            data=response_data,
            status=response_status
        )
