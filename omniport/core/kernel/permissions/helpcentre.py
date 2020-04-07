from django.conf import settings
from rest_framework.permissions import BasePermission

from kernel.utils.logs import log_permission


def has_helpcentre_rights(user):
    """
    Check if the given user has enough privileges for Helpcentre
    :param user: the user whose privileges are being tested
    :return: True if the user has privileges, False otherwise
    """

    if settings.DEBUG:
        has_permission = user.is_superuser
        log_permission('helpcentre', user, has_permission)
        return has_permission

    try:
        from shell.utils.rights import has_helpcentre_rights as helpcentre
        has_permission = helpcentre(user)
    except ImportError:
        has_permission = user.is_superuser

    log_permission('helpcentre', user, has_permission)
    return has_permission


class HasHelpcentreRights(BasePermission):
    """
    Allows access only to users who have Helpcentre rights
    """

    def has_permission(self, request, view):
        return (
                request.user is not None
                and has_helpcentre_rights(request.user)
        )
