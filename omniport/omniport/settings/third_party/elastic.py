"""
This setting file exposes settings for Elasticsearch.

Connection parameters are read from the environment so the same image
runs against:
  - dev:     a local docker-compose sidecar       (ELASTICSEARCH_HOST=http://elastic:9200)
  - prod:    a separate ES VM with TLS + auth     (ELASTICSEARCH_HOST=https://search.internal.example.com:9200)

The corresponding env file is `noticeboard/elasticsearch.env` in
omniport-docker; see `noticeboard/elasticsearch_stencil.env` there for
the full list of variables and their meanings.
"""

import os


def _bool(value):
    return str(value).strip().lower() in ('1', 'true', 'yes', 'on')


_user = os.environ.get('ELASTICSEARCH_USER', '').strip()
_password = os.environ.get('ELASTICSEARCH_PASSWORD', '').strip()
_http_auth = (_user, _password) if _user and _password else None

_default_connection = {
    'hosts': os.environ.get('ELASTICSEARCH_HOST', 'http://elastic:9200'),
    'verify_certs': _bool(os.environ.get('ELASTICSEARCH_VERIFY_CERTS', 'false')),
    'timeout': int(os.environ.get('ELASTICSEARCH_TIMEOUT', '5')),
}

if _http_auth:
    _default_connection['http_auth'] = _http_auth

_ca_cert = os.environ.get('ELASTICSEARCH_CA_CERT', '').strip()
if _ca_cert:
    _default_connection['ca_certs'] = _ca_cert

ELASTICSEARCH_DSL = {
    'default': _default_connection,
}
