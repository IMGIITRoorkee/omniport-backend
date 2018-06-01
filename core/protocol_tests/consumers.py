import json
from json import JSONDecodeError

from channels.generic.websocket import WebsocketConsumer


class PingPong(WebsocketConsumer):
    """
    Replies with a 'Pong' for every 'Ping' and a 'Ping' for every 'Pong'
    """

    def connect(self):
        """
        Process the connection request sent by a socket instance
        """

        self.accept()

    def disconnect(self, _):
        """
        Process the disconnection of a socket instance
        :param _: the code indicating the reason for disconnection
        """

        pass

    def receive(self, text_data=None, bytes_data=None):
        """
        Receive a message from a socket and then act upon it
        :param text_data: data sent by the socket instance in textual format
        :param bytes_data: data sent by the socket instance as byte stream
        """

        if text_data is None:
            return

        try:
            text_data = json.loads(text_data)
            message = text_data.get('message', None)
            if message == 'Ping':
                reply = 'Pong'
            elif message == 'Pong':
                reply = 'Ping'
            else:
                reply = message
        except JSONDecodeError:
            reply = 'An error occurred'

        self.send(text_data=json.dumps(
            {
                'message': reply,
            }
        ))
