import swapper


def get_role(person, role_name):
    """
    Get a role corresponding to a person
    :param person: an instance of the Person model whose roles are sought
    :param role_name: the name of the role class whose instance is required
    :return: the role, if the person fulfills it
    :raise: Role.DoesNotExist, if the given role is not fulfilled by the person
    :raise: ImproperlyConfigured, if the name of the role class is incorrect
    """

    Role = swapper.load_model('kernel', role_name)
    role = Role.objects.get(person=person)
    return role
