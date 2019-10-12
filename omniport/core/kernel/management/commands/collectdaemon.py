import os

from django.apps import apps
from django.conf import settings
from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    """
    This class describes the command to be executed
    """

    help = """Collect supervisord configuration scripts for all the apps and 
    services. The files are symlinked into a global directory where the
    supervisor service can read them.
    Usage: django-admin collectdaemon [APP_NAME]...
    """

    def add_arguments(self, parser):
        parser.add_argument('apps', nargs='*', type=str)

    def handle(self, *args, **options):
        successful_apps = set()
        for app in options['apps'] or apps.get_app_configs():
            if isinstance(app, str):
                app = apps.get_app_config(app)

            if not app:
                raise CommandError('Invalid application/service name')

            source = os.path.join(app.path, settings.APP_SUPERVISORD_DIR)
            configuration_files = (
                os.path.join(root, file)
                for root, _, files in os.walk(source)
                for file in files
                if file.endswith('.conf')
            )
            destination_root = settings.SUPERVISORD_DIR
            for file in configuration_files:
                print(file)
                try:
                    os.symlink(
                        file,
                        os.path.join(destination_root, os.path.basename(file))
                    )
                except OSError:
                    self.stdout.write(
                        self.style.WARNING(
                            f'Failed to fetch file {os.path.basename(file)} '
                            f'for app {app.name}'
                        )
                    )
                successful_apps.add(app.name)

        self.stdout.write(
            self.style.SUCCESS(
                f'Successfully collected daemon scripts for '
                f'{", ".join(successful_apps)}'
            )
        )
