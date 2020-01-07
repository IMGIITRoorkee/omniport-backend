import logging

logger = logging.getLogger('kernel_permissions')


def log_permission(permission_name, user, is_allowed):
    """
    Form sentences to log requests for kernel permissions
    This takes the name of the permission, the user who made the request, and
    whether the user was allowed or not, logs a relevant message with
    appropriate level.
    :param permission_name: the kernel permission to be logged
    :param user: user requesting the permission
    :param is_allowed: whether the user was allowed or not
    """

    log_type = 'info' if is_allowed else 'warning'
    getattr(logger, log_type)(
        f'[{permission_name.upper()}] '
        f'User {user}({user.id}) was{" " if is_allowed else " not "}'
        f'given {permission_name} rights'
    )
