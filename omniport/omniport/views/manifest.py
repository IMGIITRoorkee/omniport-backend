import os

from django.conf import settings
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response


class Manifest(GenericAPIView):
    """
    This view returns the dynamically generated manifest for the Omniport PWA
    """

    renderer_classes = [
        JSONRenderer,
    ]

    @staticmethod
    def get_url(directory, item):
        """
        Get the URL to the given imagery item
        :param directory: the directory in which the imagery resides
        :param item: the item whose URL is to be determined
        :return: the URL to the item
        """

        return os.path.join(
            directory,
            item
        ).replace(
            f'{settings.BRANDING_ROOT}/',
            settings.BRANDING_URL
        )

    def get(self, request, *args, **kwargs):
        """
        View to serve GET requests
        :param request: the request that is to be responded to
        :param args: arguments
        :param kwargs: keyword arguments
        :return: the response for request
        """

        icons = list()
        if settings.SITE.imagery.logo_512:
            icons.append({
                'src': Manifest.get_url(
                    settings.SITE.imagery.directory,
                    settings.SITE.imagery.logo_512
                ),
                'type': settings.SITE.imagery.logo_512_mime,
                'sizes': '512x512',
            })
        if settings.SITE.imagery.logo_192:
            icons.append({
                'src': Manifest.get_url(
                    settings.SITE.imagery.directory,
                    settings.SITE.imagery.logo_192
                ),
                'type': settings.SITE.imagery.logo_192_mime,
                'sizes': '192x192',
            })
        if settings.SITE.imagery.logo:
            icons.append({
                'src': Manifest.get_url(
                    settings.SITE.imagery.directory,
                    settings.SITE.imagery.logo
                ),
                'type': settings.SITE.imagery.logo_mime,
                'sizes': '48x48 96x96 128x128 192x192 256x256 512x512',
            })

        response = {
            # Nomenclature
            'short_name': settings.SITE.nomenclature.verbose_name,
            'name': settings.SITE.nomenclature.verbose_name,
            'description': settings.SITE.description,

            # Iconography
            'icons': icons,

            # URLs
            'scope': '/',
            'start_url': '/',

            # Display
            'display': 'standalone',
            'orientation': 'portrait',

            # Theming
            'background_color': '#282c35',
            'theme_color': '#ee1d51',
        }
        return Response(response, status=status.HTTP_200_OK)
