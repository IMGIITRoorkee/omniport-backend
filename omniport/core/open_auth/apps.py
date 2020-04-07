from django.apps import AppConfig


class OpenAuthConfig(AppConfig):
    name = 'open_auth'
    verbose_name = 'OAuth2-based authentication'

    def ready(self):
        import open_auth.signals
