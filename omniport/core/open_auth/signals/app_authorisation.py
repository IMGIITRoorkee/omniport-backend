from oauth2_provider.signals import app_authorized

from open_auth.utils import send_authorisation_notification


def handle_app_authorized(sender, request, token, **kwargs):
    person = token.user.person
    if person is None:
        pass
    else:
        send_authorisation_notification(token.application.name, person.id)


app_authorized.connect(handle_app_authorized)
