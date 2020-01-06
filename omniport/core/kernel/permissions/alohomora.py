from django.conf import settings
from rest_framework.permissions import BasePermission

from kernel.utils.logs import log_permission


def has_alohomora_rights(user):
    """
    Check if the given user has enough privileges for Alohomora
    :param user: the user whose privileges are being tested
    :return: True if the user has privileges, False otherwise
    """

    if settings.DEBUG:
        has_permission = user.is_superuser
        log_permission('alohomora', user, has_permission)
        return has_permission

    try:
        from shell.utils.rights import has_alohomora_rights as alohomora
        has_permission = alohomora(user)
    except ImportError:
        has_permission = user.is_superuser

    log_permission('alohomora', user, has_permission)
    return has_permission


class HasAlohomoraRights(BasePermission):
    """
    Allows access only to users who have Alohomora rights
    """

    def has_permission(self, request, view):
        return (
                request.user is not None
                and has_alohomora_rights(request.user)
        )
