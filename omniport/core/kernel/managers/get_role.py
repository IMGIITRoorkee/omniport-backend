import swapper
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured, ObjectDoesNotExist

from formula_one.mixins.period_mixin import ActiveStatus


def get_role(person, role_name, active_status=ActiveStatus.ANY, silent=False, *args, **kwargs):
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

    is_custom_role = kwargs.get('is_custom_role', False)

    try:
        if is_custom_role:
            Role = swapper.load_model(
                role_name.split('.')[0],
                role_name.split('.')[1],
            )
        else:
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


def get_all_roles(person):
    """
    Get all roles corresponding to a person
    :param person: an instance of the Person model whose roles are sought
    :return: a dictionary of all roles mapped to their instance and ActiveStatus
    """

    all_roles = dict()
    roles = settings.ROLES
    for role_name in roles:
        try:
            role = get_role(
                person=person,
                role_name=role_name,
                active_status=ActiveStatus.ANY,
                silent=False,
                is_custom_role='.' in role_name,
            )
            active_status = role.active_status
            all_roles[role_name] = {
                'instance': role,
                'activeStatus': active_status,
            }
        except ObjectDoesNotExist:
            pass
    return all_roles
