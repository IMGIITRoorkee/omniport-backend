from rest_framework.permissions import BasePermission

class TokenHasPermissionKey(BasePermission):
    """
    Check if the given app access token is authenticated for the permission key
    of the view
    """

    def has_permission(self, request, view):
        permission_key = view.permission_key
        app_access_token = request.user
        try:
            has_permission_key = permission_key in app_access_token.permission_keys
            return has_permission_key
        except Exception:
            return False
