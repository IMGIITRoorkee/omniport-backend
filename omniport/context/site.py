from django.conf import settings


def site_information(request):
    """
    Add the site information from settings to the context
    :param request: the request being served
    :return: the data to add to the context
    """

    data = dict()
    data['SITE_NAME'] = settings.SITE_NAME
    data['SITE_VERBOSE_NAME'] = settings.SITE_VERBOSE_NAME
    return data
