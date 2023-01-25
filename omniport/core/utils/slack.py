import requests
from django.core.exceptions import ImproperlyConfigured

from omniport.settings.configuration.base import CONFIGURATION


def get_slack_md_section(md_text):
    """
    This function wraps a markdown string as a slack markdown section
    :param md_text: markdown_text
    :return: Slack section block
    """
    return {
        'type': 'section',
        'text': {
            'type': 'mrkdwn',
            'text': md_text
        }
    }


def get_slack_app_config(slack_app):
    """
    This function fetches the configuration for a given Slack app
    :param slack_app: name of the Slack app
    :return: Slack app configuration
    """

    slack = CONFIGURATION.integrations.get('slack', None)
    error_message = f'Slack App not configured for {slack_app}'

    if slack:
        app_config = slack.get(slack_app, None)
        if app_config and app_config.get('url', None):
            return app_config

        raise ImproperlyConfigured(error_message)

    raise ImproperlyConfigured(error_message)


def send_slack_notification(slack_app, message):
    """
    This function is used to send notifications via a Slack app
    :param slack_app: name of the Slack app
    :param message: formatted notification message for the Slack app
    """

    app_config = get_slack_app_config(slack_app)

    response = requests.post(app_config.get('url'), json=message)
    response.raise_for_status()
