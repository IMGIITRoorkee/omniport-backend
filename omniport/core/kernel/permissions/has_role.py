from rest_framework.permissions import BasePermission

from kernel.managers.get_role import get_role
from kernel.mixins.period_mixin import ActiveStatus


def get_has_role(role_name):
    """
    Returns a permission class that checks if a person has a specific role
    :param role_name: the name of the role to check for
    :return: a permission class that can be used with DRF
    """

    class HasRole(BasePermission):
        """
        Allows access only to users having the given role
        """

        def has_permission(self, request, view):
            return get_role(
                person=request.person,
                role_name=role_name,
                active_status=ActiveStatus.IS_ACTIVE,
                silent=True
            ) is not None

    return HasRole
