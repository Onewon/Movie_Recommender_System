from __future__ import absolute_import, unicode_literals
import os
from celery import Celery, platforms
#add
from django.conf import settings
#

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'MRS.settings')

# app = Celery('MRS')
app = Celery('MRS', backend='redis', broker='redis://localhost:6379/0')

# Using a string here means the worker don't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
#app.config_from_object('django.conf:settings', namespace='CELERY')
app.config_from_object('django.conf:settings')
# Load task modules from all registered Django app configs.
app.autodiscover_tasks(settings.INSTALLED_APPS) #                add apps

# 允许root 用户运行celery
platforms.C_FORCE_ROOT = True

@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))
