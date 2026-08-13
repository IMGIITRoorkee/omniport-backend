import datetime

from omniport.utils import switcher

from kernel.managers.get_role import get_all_roles
from notifications.actions import push_notification
from categories.models import Category


AvatarSerializer = switcher.load_serializer('kernel', 'Person', 'Avatar')


def _resolve_path(root, dotted_path):
    """
    Safely walk a dotted attribute path starting from ``root`` without using
    eval(). A path segment ending in ``()`` is treated as a no-argument method
    call, which is required for paths such as ``contact_information.first()``.
    Returns ``None`` if any segment along the way is missing or is ``None``.
    :param root: the object to start traversal from
    :param dotted_path: the dotted attribute path to resolve
    :return: the resolved value, or None if it cannot be resolved
    """

    obj = root
    for segment in dotted_path.split('.'):
        if obj is None:
            return None
        if segment.endswith('()'):
            method = getattr(obj, segment[:-2], None)
            if not callable(method):
                return None
            obj = method()
        else:
            obj = getattr(obj, segment, None)
    return obj


def get_field_data(person, field_data_points, object_string):
    """
    Utility function to get requested model's data
    :param person: person object whose data is to be retrieved
    :param field_data_points: the specific fields of a model to be retrieved
    :param object_string: object variable name to access the data
    :return: data for a model string
    """

    # ``object_string`` is a dotted path rooted at the ``person`` object
    # (e.g. 'person', 'person.student', 'person.contact_information.first()').
    # ``field_data_points`` originate from OAuth application configuration and
    # are therefore untrusted, so the value is resolved by safe attribute
    # traversal rather than eval() to avoid remote code execution (CWE-95).
    data = dict()

    if object_string == 'person':
        base_object = person
    elif object_string.startswith('person.'):
        base_object = _resolve_path(person, object_string[len('person.'):])
    else:
        base_object = None

    if base_object is None:
        return data

    for field_data_point in field_data_points:
        data[f'{field_data_point.replace(".", " ")}'] = \
            _resolve_path(base_object, field_data_point)
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


def get_custom_roles(person):
    """
    Get all the custom roles of a person in convenient list format
    :param person: the person whose custom roles are being retrieved
    :return: the custom roles of the person as a list
    """

    roles = get_all_roles(person)
    custom_roles = [
        {
            'role': role,
            'activeStatus': str(roles[role]['activeStatus']),
        }
        for role in roles if '.' in role
    ]
    return custom_roles


def get_display_picture(person):
    """
    Utility function to return path to display picture of user
    :param person: person object whose display picture path to be retrieved
    :return: path to the display picture
    """

    return AvatarSerializer(person).data['display_picture']


def get_category():
    """
    Get or create Category instance with slug
    :return: the found or newly created Category object
    """

    service_name = 'open_auth'
    service_verbose = 'OAuth 2.0'
    category, _ = Category.objects.get_or_create(
        slug=service_name,
        name=service_verbose,
    )
    return category


def send_authorisation_notification(application_name, person_id):
    """
    Send notification to the user whenever logged in with the OAuth
    :param application_name: name of the application
    :param person_id: id of the person logged in
    :return: notification
    """

    print(f'You logged in into {application_name} on {datetime.datetime.now().strftime(" %b %d, %Y, %I: %M %p")}.', person_id)

    push_notification(
        template=f'You logged in into {application_name} on '
        f'{datetime.datetime.now().strftime("%b %d, %Y, %I: %M %p")}.',
        category=get_category(),
        web_onclick_url='',
        android_onclick_activity='',
        ios_onclick_action='',
        is_personalised=True,
        person=person_id,
        has_custom_users_target=False,
        persons=None,
    )
