from django.shortcuts import render
from django.views import View


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
            template_name='omniport/ping_pong.html',
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
