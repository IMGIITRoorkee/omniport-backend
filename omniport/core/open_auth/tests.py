import base64

from django.core.cache import cache
from django.test import SimpleTestCase, override_settings
from rest_framework.request import Request
from rest_framework.test import APIRequestFactory

from open_auth.views.throttling import OAuthClientThrottle, OAuthFailureThrottle


class ThreePerHourThrottle(OAuthClientThrottle):
    THROTTLE_RATES = {'open_auth': '3/hour'}


class ThreeFailuresThrottle(OAuthFailureThrottle):
    THROTTLE_RATES = {'open_auth_failures': '3/hour'}


class Rejection:
    def __init__(self, content, status_code=400):
        self.content = content
        self.status_code = status_code


@override_settings(CACHES={'default': {
    'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
}})
class OAuthClientThrottleTests(SimpleTestCase):
    """
    Tests that the throttle counts a client application, and not an address
    """

    def setUp(self):
        cache.clear()
        self.factory = APIRequestFactory()

    def token_request(self, client_id=None, ip='10.0.0.1', **extra):
        body = {'grant_type': 'authorization_code'}
        if client_id:
            body['client_id'] = client_id
        return Request(self.factory.post(
            '/open_auth/token/', body, REMOTE_ADDR=ip, **extra
        ))

    def allow(self, client_id=None, ip='10.0.0.1', **extra):
        request = self.token_request(client_id, ip, **extra)
        return ThreePerHourThrottle().allow_request(request, None)

    def test_clients_sharing_an_address_are_counted_apart(self):
        for _ in range(3):
            self.assertTrue(self.allow('election'))
        self.assertFalse(self.allow('election'))
        self.assertTrue(self.allow('noticeboard'))

    def test_one_client_is_counted_across_addresses(self):
        for ip in ('10.0.0.1', '10.0.0.2', '10.0.0.3'):
            self.assertTrue(self.allow('election', ip))
        self.assertFalse(self.allow('election', '10.0.0.4'))

    def test_a_client_naming_itself_in_the_header_is_counted(self):
        credentials = base64.b64encode(b'election:secret').decode()
        for _ in range(3):
            self.assertTrue(
                self.allow(HTTP_AUTHORIZATION=f'Basic {credentials}')
            )
        self.assertFalse(self.allow('election'))

    def test_a_throttled_client_is_told_when_to_retry(self):
        throttle = ThreePerHourThrottle()
        for _ in range(4):
            allowed = throttle.allow_request(self.token_request('election'), None)

        self.assertFalse(allowed)
        self.assertGreater(throttle.wait(), 0)

    def test_a_client_that_only_succeeds_is_never_failure_throttled(self):
        for _ in range(10):
            self.assertTrue(
                ThreeFailuresThrottle().allow_request(
                    self.token_request('election'), None
                )
            )

    def test_failures_are_counted_until_the_client_is_refused(self):
        for _ in range(3):
            request = self.token_request('election')
            self.assertTrue(ThreeFailuresThrottle().allow_request(request, None))
            ThreeFailuresThrottle().count(request)

        self.assertFalse(
            ThreeFailuresThrottle().allow_request(
                self.token_request('election'), None
            )
        )
        self.assertTrue(
            ThreeFailuresThrottle().allow_request(
                self.token_request('noticeboard'), None
            )
        )

    def test_a_stranger_cannot_spend_the_allowance_of_a_client(self):
        for _ in range(3):
            ThreeFailuresThrottle().count(
                self.token_request('election', '203.0.113.9')
            )

        self.assertFalse(
            ThreeFailuresThrottle().allow_request(
                self.token_request('election', '203.0.113.9'), None
            )
        )
        self.assertTrue(
            ThreeFailuresThrottle().allow_request(
                self.token_request('election', '10.0.0.1'), None
            )
        )

    def test_only_a_client_that_cannot_prove_itself_is_counted(self):
        counted = ThreeFailuresThrottle.is_credential_failure
        self.assertTrue(counted(Rejection(b'{"error": "invalid_client"}')))
        self.assertTrue(counted(Rejection(b'', status_code=401)))
        self.assertFalse(counted(Rejection(b'{"error": "invalid_grant"}')))
        self.assertFalse(counted(Rejection(b'', status_code=302)))
