"""
Elasticsearch signal handling that cannot take a database write down with it
"""

import logging

from django_elasticsearch_dsl.signals import RealTimeSignalProcessor

logger = logging.getLogger('django')


class ForgivingSignalProcessor(RealTimeSignalProcessor):
    """
    Keep indexed documents in step with the database, without letting the
    cluster decide whether the write that triggered them is allowed to succeed
    """

    def _log_failure(self, action, instance, exc):
        logger.warning(
            'Elasticsearch %s failed for %s(pk=%s): %s. The database write '
            'stands and the index is repaired by search_index --rebuild.',
            action,
            type(instance).__name__,
            getattr(instance, 'pk', None),
            exc,
            exc_info=True,
        )

    def handle_save(self, sender, instance, **kwargs):
        try:
            super().handle_save(sender, instance, **kwargs)
        except Exception as exc:
            self._log_failure('save', instance, exc)

    def handle_pre_delete(self, sender, instance, **kwargs):
        try:
            super().handle_pre_delete(sender, instance, **kwargs)
        except Exception as exc:
            self._log_failure('pre-delete', instance, exc)

    def handle_delete(self, sender, instance, **kwargs):
        try:
            super().handle_delete(sender, instance, **kwargs)
        except Exception as exc:
            self._log_failure('delete', instance, exc)

    def handle_m2m_changed(self, sender, instance, action, **kwargs):
        try:
            super().handle_m2m_changed(sender, instance, action, **kwargs)
        except Exception as exc:
            self._log_failure('m2m change', instance, exc)


__all__ = [
    'ForgivingSignalProcessor',
]
