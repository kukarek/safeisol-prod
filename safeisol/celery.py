from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

"""
Celery application configuration for the 'safeisol' Django project.
This module sets up the Celery app instance, configures it to use Django's settings,
and automatically discovers tasks from all installed Django apps.
- Sets the default Django settings module for the 'celery' command-line program.
- Initializes the Celery application with the project name 'safeisol'.
- Loads Celery configuration from Django settings, using the 'CELERY_' namespace.
- Autodiscover tasks from all registered Django app configs.
Usage:
    Import the 'app' object in your Celery worker or manage.py to ensure
    the Celery app is loaded with the correct Django context.
"""

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'safeisol.settings')

app = Celery('safeisol')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()