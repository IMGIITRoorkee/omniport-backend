import swapper
from django.core.exceptions import ImproperlyConfigured


def get_role(person, role_name, filter_active=True, silent=False):
    """
    Get a role corresponding to a person
    :param person: an instance of the Person model whose roles are sought
    :param role_name: the name of the role class whose instance is required
    :param filter_active: whether to filter out the roles other than active
    :param silent: whether to fail silently or raise exceptions
    :return: the role, if the person fulfills it
    :raise: Role.DoesNotExist, if the given role is not fulfilled by the person
    :raise: ImproperlyConfigured, if the name of the role class is incorrect
    """

    try:
        Role = swapper.load_model('kernel', role_name)
        try:
            if filter_active:
                query_set = Role.all_filter_active()
            else:
                query_set = Role.objects.all()
            role = query_set.get(person=person)
            return role
        except Role.DoesNotExist:
            if not silent:
                raise
    except ImproperlyConfigured:
        if not silent:
            raise

    return None
