from django.conf import settings


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
