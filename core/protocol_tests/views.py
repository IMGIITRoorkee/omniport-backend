import datetime

from django.shortcuts import render
from django.views import View
from rest_framework.response import Response
from rest_framework.views import APIView


class HelloWorld(APIView):
    """
    This view greets visitors with a friendly 'Hello World!'
    """

    @staticmethod
    def hello_world():
        """
        Return a 'Hello World!' message in JSON format
        :return: a 'Hello World!' message in JSON format
        """

        response = {
            'message': 'Hello World!',
            'timestamp': datetime.datetime.now(),
        }
        return Response(response)

    @staticmethod
    def get(_, *__, **___):
        """
        Return a 'Hello World!' message in JSON format
        :param _: the request for which response is being sent
        :param __: additional arguments
        :param ___: additional keyword arguments
        :return: a 'Hello World!' message in JSON format
        """

        return HelloWorld.hello_world()


class PingPong(View):
    """
    This view greets visitors with two buttons, to send 'Ping' and 'Pong' to the
    server which sends the opposite reply
    """

    @staticmethod
    def ping_pong(request):
        """
        Return the rendered HTML page with buttons to send 'Ping' and 'Pong'
        :param request: the request for which response is being sent
        :return: the rendered HTML page with buttons to send 'Ping' and 'Pong'
        """

        return render(
            request=request,
            template_name='ping_pong/ping_pong.html',
            context=None
        )

    @staticmethod
    def get(request, *_, **__):
        """
        Return the rendered HTML page with buttons to send 'Ping' and 'Pong'
        :param request: the request for which response is being sent
        :param _: additional arguments
        :param __: additional keyword arguments
        :return: the rendered HTML page with buttons to send 'Ping' and 'Pong'
        """

        return PingPong.ping_pong(request)
