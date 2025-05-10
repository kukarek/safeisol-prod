from __future__ import absolute_import, unicode_literals

# Это позволяет Django автоматически подхватывать celery при запуске
from .celery import app as celery_app

__all__ = ('celery_app',)