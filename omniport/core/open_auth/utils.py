from omniport.utils import switcher


AvatarSerializer = switcher.load_serializer('kernel', 'Person', 'Avatar')


def get_field_data(person, field_data_points, model_string):
    """
    Utility function to get requested model's data
    :param person: person object whose data is to be retrieved
    :param field_data_points: the specific fields of a model to be retrieved
    :param model_string: model name string to access the data
    :return: data for a model string
    """

    data = dict()
    if eval(model_string) is None:
        return data
    for field_data_point in field_data_points:
        data[f'{field_data_point.replace(".", " ")}'] = \
            eval(f'{model_string}.{field_data_point}')
    return data


def get_roles(person):
    """
    Utility function to return the name and active status of person's roles
    :param person: person object whose roles are to be retrieved
    :return: roles for a person
    """

    all_roles = AvatarSerializer(person).data['roles']
    for role in all_roles:
        role.pop('data', None)
    return all_roles


def get_display_picture(person):
    """
    Utility function to return path to display picture of user
    :param person: person object whose display picture path to be retrieved
    :return: path to the display picture
    """

    return AvatarSerializer(person).data['display_picture']
