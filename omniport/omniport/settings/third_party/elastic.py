'''
This setting file exposes settings for Elastic search
'''

ELASTICSEARCH_DSL = {
    "default": {
        "hosts": "http://elastic:9200",
        # "http_auth": ("elastic", "P5jr_rdNiFlQp_FkDtKm"),
        "verify_certs": False,
    }
}