from django.conf import settings

from configuration.serializers.project.branding import BrandSerializer
from configuration.serializers.project.site import SiteSerializer


def branding_site(_=None):
    """
    Add the branding of the site to the context
    :param _: the request being served
    :return: the data to add to the context
    """

    data = {
        'site': SiteSerializer(settings.SITE).data,
    }
    return data


def branding_maintainers(_=None):
    """
    Add the branding of the maintainers to the context
    :param _: the request being served
    :return: the data to add to the context
    """

    data = {
        'maintainers': BrandSerializer(settings.MAINTAINERS).data,
    }
    return data


def branding_institute(_=None):
    """
    Add the branding of the institute to the context
    :param _: the request being served
    :return: the data to add to the context
    """

    data = {
        'institute': BrandSerializer(settings.INSTITUTE).data,
    }
    return data
