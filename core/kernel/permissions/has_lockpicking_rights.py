from rest_framework.permissions import BasePermission

from kernel.utils.rights import has_lockpicking_rights


class HasLockpickingRights(BasePermission):
    """
    Allows access only to users who have lockpicking rights
    """

    def has_permission(self, request, view):
        return request.user is not None and has_lockpicking_rights(request.user)
