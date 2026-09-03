"""
This setting file exposes settings for Elasticsearch.

Connection parameters are read from the environment so the same image
runs against:
  - dev:     a local docker-compose sidecar       (ELASTICSEARCH_HOST=http://elasticsearch:9200)
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

# The fallback names the docker-compose sidecar, so it has to match the
# service in the compose file rather than read well: an unresolvable default
# fails as a connection error, which the noticeboard search catches and
# answers from PostgreSQL instead, leaving a developer with search that looks
# like it works and never touches the cluster.
_host = os.environ.get(
    'ELASTICSEARCH_HOST',
    'http://elasticsearch:9200',
).strip()

# Certificate checking follows the scheme unless the environment overrides it.
# A fixed default of false is the wrong way round for a deployment that talks
# https and forgets the flag, because that is TLS nobody is checking, which
# looks identical to the real thing until someone is in the middle of it.
_verify_certs_default = 'true' if _host.lower().startswith('https://') else 'false'

_default_connection = {
    'hosts': _host,
    'verify_certs': _bool(
        os.environ.get('ELASTICSEARCH_VERIFY_CERTS', _verify_certs_default),
    ),
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

# Indexing runs inside the request that saved the model, so the stock processor
# lets a cluster that is down, full or slow turn an ordinary save into a 500.
# Search already answers from PostgreSQL when the cluster is unreachable, and
# writes degrade the same way here: the row is saved, the failure is logged, and
# search_index --rebuild repairs whatever the index missed.
ELASTICSEARCH_DSL_SIGNAL_PROCESSOR = (
    'omniport.utils.elasticsearch.ForgivingSignalProcessor'
)
