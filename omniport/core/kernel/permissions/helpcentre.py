from django.conf import settings


def has_helpcentre_rights(user):
    """
    Check if the given user has enough privileges for Helpcentre
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
