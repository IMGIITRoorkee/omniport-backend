from django.conf import settings
from rest_framework import generics
from rest_framework import response
from rest_framework import status

from configuration.serializers.project.branding import BrandSerializer
from configuration.serializers.project.site import SiteSerializer


class SiteBrandingView(generics.GenericAPIView):
    """
    Provide the branding information of the site as JSON to the frontend
    """

    serializer_class = SiteSerializer

    def get(self, request, *args, **kwargs):
        """
        View to serve GET requests
        :param request: the request that is to be responded to
        :param args: arguments
        :param kwargs: keyword arguments
        :return: the response for request
        """

        response_dict = self.get_serializer(instance=settings.SITE).data
        return response.Response(response_dict, status=status.HTTP_200_OK)


class InstituteBrandingView(generics.GenericAPIView):
    """
    Provide the branding information of the institute as JSON to the frontend
    """

    serializer_class = BrandSerializer

    def get(self, request, *args, **kwargs):
        """
        View to serve GET requests
        :param request: the request that is to be responded to
        :param args: arguments
        :param kwargs: keyword arguments
        :return: the response for request
        """

        response_dict = self.get_serializer(instance=settings.INSTITUTE).data
        return response.Response(response_dict, status=status.HTTP_200_OK)


class MaintainersBrandingView(generics.GenericAPIView):
    """
    Provide the branding information of the maintainers as JSON to the frontend
    """

    serializer_class = BrandSerializer

    def get(self, request, *args, **kwargs):
        """
        View to serve GET requests
        :param request: the request that is to be responded to
        :param args: arguments
        :param kwargs: keyword arguments
        :return: the response for request
        """

        response_dict = self.get_serializer(instance=settings.MAINTAINERS).data
        return response.Response(response_dict, status=status.HTTP_200_OK)
