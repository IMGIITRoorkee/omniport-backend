"""
These functions are an essential part of the rights framework used by Omniport.
They determine which users have access to the administrative features of the
project, namely
- omnipotence, the admin interface
- alohomora, the impersonation ability
- lockpicking, the no-questions-asked password reset ability
- helpcentre, the ability to access and answer user queries

These can, and most probably should, be overridden in shell.utils.rights
"""

from django.conf import settings


def has_omnipotence_rights(user):
    """
    Check if the given user has enough privileges to access the admin interface
    :param user: the user whose privileges are being tested
    :return: True if the user has privileges, False otherwise
    """

    if settings.DEBUG:
        return user.is_superuser

    try:
        from shell.utils.rights import has_omnipotence_rights as omnipotence
        return omnipotence(user)
    except ImportError:
        return user.is_superuser


def has_alohomora_rights(user):
    """
    Check if the given user has enough privileges to impersonate another user
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


def has_lockpicking_rights(user):
    """
    Check if the given user has enough privileges to reset anyone's password
    :param user: the user whose privileges are being tested
    :return: True if the user has privileges, False otherwise
    """

    if settings.DEBUG:
        return user.is_superuser

    try:
        from shell.utils.rights import has_lockpicking_rights as lockpicking
        return lockpicking(user)
    except ImportError:
        return user.is_superuser


def has_helpcentre_rights(user):
    """
    Check if the given user has enough privileges to access helpcentre
    :param user: the user whose privileges are being tested
    :return: True if the user has privileges, False otherwise
    """

    if settings.DEBUG:
        return user.is_superuser

    try:
        from shell.utils.rights import has_helpcentre_rights as helpcentre
        return helpcentre(user)
    except ImportError:
        return user.is_superuser
