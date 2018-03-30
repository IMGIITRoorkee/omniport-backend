from rest_framework.response import Response
from rest_framework.views import APIView


class Placeholder(APIView):
    """
    This view shows a placeholder message "Coming soon!"
    """

    @staticmethod
    def coming_soon():
        """
        Return a 'Coming soon!' message in JSON format
        :return: a 'Coming soon!' message in JSON format
        """

        response = {
            'data': {
                'type': 'message',
                'attributes': {
                    'text': 'Coming soon!',
                    'subtext': 'This view is under development and will be '
                               'live very soon, so stay tuned',
                },
            },
        }
        return Response(response)

    @staticmethod
    def get(_, *__, **___):
        """
        Return a 'Coming soon!' message in JSON format
        :param _: the request for which response is being sent
        :param __: additional arguments
        :param ___: additional keyword arguments
        :return: a 'Coming soon!' message in JSON format
        """

        return Placeholder.coming_soon()
