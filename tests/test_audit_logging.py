"""
Tests for the namespaces the request audit trail covers

These import the middleware directly rather than through Django, so they run
in a bare interpreter with no settings module and no database.
"""

import pathlib
import sys
import types
import unittest
import unittest.mock

import django.conf

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / 'omniport'))

# localdate() reads these two; nothing else here touches the settings module
if not django.conf.settings.configured:
    django.conf.settings.configure(USE_TZ=True, TIME_ZONE='Asia/Kolkata')

from omniport.constants import APP_ENTRY_SESSION_KEY
from omniport.middleware.auth_security import AuditLoggingMiddleware


# Two discovered names and one authentication namespace, which never is one
DISCOVERED = frozenset({'bhawan_app', 'common_biodata'})


def middleware_over(namespaces=DISCOVERED):
    """
    An instance built without __init__, which would need live settings
    """

    middleware = AuditLoggingMiddleware.__new__(AuditLoggingMiddleware)
    middleware.namespaces = namespaces
    return middleware


def request_for(app_name):
    """
    Build the smallest stand-in for a request that the predicate reads, where
    an app_name of None is a path that resolved to no view at all
    """

    resolver_match = (
        None if app_name is None else types.SimpleNamespace(app_name=app_name)
    )
    return types.SimpleNamespace(resolver_match=resolver_match)


class StubSession(dict):
    """
    A session that records nothing more than the middleware reads from one
    """

    def __init__(self, session_key='a-session-key'):
        super().__init__()
        self.session_key = session_key


class AppEntryTestCase(unittest.TestCase):
    """
    Tests for AuditLoggingMiddleware.log_app_entry
    """

    def setUp(self):
        self.logged = []
        self.middleware = AuditLoggingMiddleware.__new__(AuditLoggingMiddleware)
        self.session = StubSession()
        self.request = types.SimpleNamespace(session=self.session)

    def enter(self, app_name):
        with unittest.mock.patch(
            'omniport.middleware.auth_security.auth_security_log',
            lambda message, level, user: self.logged.append(message),
        ):
            self.middleware.log_app_entry(self.request, app_name, user=object())

    def test_first_entry_is_logged(self):
        self.enter('bhawan_app')
        self.assertEqual(self.logged, ['Opened bhawan_app'])

    def test_repeat_entry_the_same_day_is_not_logged(self):
        for _ in range(5):
            self.enter('bhawan_app')
        self.assertEqual(self.logged, ['Opened bhawan_app'])

    def test_a_second_app_is_logged_separately(self):
        self.enter('bhawan_app')
        self.enter('noticeboard')
        self.assertEqual(
            self.logged, ['Opened bhawan_app', 'Opened noticeboard']
        )

    def test_a_new_day_is_logged_again(self):
        self.enter('bhawan_app')
        self.session[APP_ENTRY_SESSION_KEY]['bhawan_app'] = '1970-01-01'
        self.enter('bhawan_app')
        self.assertEqual(self.logged, ['Opened bhawan_app'] * 2)

    def test_a_request_without_a_session_is_not_logged(self):
        self.request.session = StubSession(session_key=None)
        self.enter('bhawan_app')
        self.assertEqual(self.logged, [])


class DiscoveredNamespaceTestCase(unittest.TestCase):
    """
    Tests for AuditLoggingMiddleware.discovered_namespace
    """

    def setUp(self):
        self.middleware = middleware_over()

    def test_every_discovered_name_is_covered(self):
        for namespace in DISCOVERED:
            with self.subTest(namespace=namespace):
                self.assertEqual(
                    self.middleware.discovered_namespace(
                        request_for(namespace)
                    ),
                    namespace,
                )

    def test_undiscovered_name_is_not_covered(self):
        self.assertIsNone(
            self.middleware.discovered_namespace(request_for('nonesuch'))
        )

    def test_unresolved_path_is_not_covered(self):
        self.assertIsNone(
            self.middleware.discovered_namespace(request_for(None))
        )

    def test_authentication_namespace_is_never_covered(self):
        """
        These lines keep the query string, which for an authentication app
        would write OAuth codes and tokens to disk. The core auth apps live
        outside the discovered directories today; this refuses them anyway,
        so the protection does not rest on where a directory happens to sit
        """

        middleware = middleware_over(DISCOVERED | {'open_auth'})
        self.assertIsNone(
            middleware.discovered_namespace(request_for('open_auth'))
        )



if __name__ == '__main__':
    unittest.main()
