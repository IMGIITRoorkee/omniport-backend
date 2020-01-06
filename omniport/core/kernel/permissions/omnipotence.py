from django.conf import settings

from kernel.utils.logs import log_permission


def has_omnipotence_rights(user):
    """
    Check if the given user has enough privileges for Omnipotence
    :param user: the user whose privileges are being tested
    :return: True if the user has privileges, False otherwise
    """

    if settings.DEBUG:
        has_permission = user.is_superuser
        log_permission('omnipotence', user, has_permission)
        return has_permission

    try:
        from shell.utils.rights import has_omnipotence_rights as omnipotence
        has_permission = omnipotence(user)
    except ImportError:
        has_permission = user.is_superuser

    log_permission('omnipotence', user, has_permission)
    return has_permission
