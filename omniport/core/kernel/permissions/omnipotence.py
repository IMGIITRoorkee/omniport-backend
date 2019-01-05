from django.conf import settings


def has_omnipotence_rights(user):
    """
    Check if the given user has enough privileges for Omnipotence
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
