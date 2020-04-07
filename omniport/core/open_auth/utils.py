import datetime

from omniport.utils import switcher

from notifications.actions import push_notification
from categories.models import Category


AvatarSerializer = switcher.load_serializer('kernel', 'Person', 'Avatar')


def get_field_data(person, field_data_points, object_string):
    """
    Utility function to get requested model's data
    :param person: person object whose data is to be retrieved
    :param field_data_points: the specific fields of a model to be retrieved
    :param object_string: object variable name to access the data
    :return: data for a model string
    """

    data = dict()
    if eval(object_string) is None:
        return data
    for field_data_point in field_data_points:
        data[f'{field_data_point.replace(".", " ")}'] = \
            eval(f'{object_string}.{field_data_point}')
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
