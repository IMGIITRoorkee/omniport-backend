import swapper
from django.core.exceptions import ImproperlyConfigured

from kernel.mixins.period_mixin import ActiveStatus


def get_role(person, role_name, active_status=ActiveStatus.ANY, silent=False):
    """
    Get a role corresponding to a person
    :param person: an instance of the Person model whose roles are sought
    :param role_name: the name of the role class whose instance is required
    :param active_status: whether the role was, is, isn't or will be active
    :param silent: whether to fail silently or raise exceptions
    :return: the role, if the person fulfills it
    :raise: Role.DoesNotExist, if the given role is not fulfilled by the person
    :raise: ImproperlyConfigured, if the name of the role class is incorrect
    """

    try:
        Role = swapper.load_model('kernel', role_name)
        try:
            query_set = Role.objects_filter(active_status)
            role = query_set.get(person=person)
            return role
        except Role.DoesNotExist:
            if not silent:
                raise
    except ImproperlyConfigured:
        if not silent:
            raise

    return None
