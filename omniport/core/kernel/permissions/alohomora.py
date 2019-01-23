from django.conf import settings
from rest_framework.permissions import BasePermission


def has_alohomora_rights(user):
    """
    Check if the given user has enough privileges for Alohomora
    :param user: the user whose privileges are being tested
    :return: True if the user has privileges, False otherwise
    """

    if settings.DEBUG:
        return user.is_superuser

    try:
        from shell.utils.rights import has_alohomora_rights as alohomora
        return alohomora(user)
    except ImportError:
        return user.is_superuser


class HasAlohomoraRights(BasePermission):
    """
    Allows access only to users who have Alohomora rights
    """

    def has_permission(self, request, view):
        return (
                request.user is not None
                and has_alohomora_rights(request.user)
        )
