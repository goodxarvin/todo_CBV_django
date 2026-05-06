import os

# from accounts.tasks import delete_objectives_every_10_second
from celery import Celery

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'todo_core.settings')

app = Celery('todo_core')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django apps.
app.autodiscover_tasks()


# @app.on_after_configure.connect
# def setup_periodic_tasks(sender: Celery, **kwargs):
#     sender.add_periodic_task(10.0, delete_objectives_every_10_second.s(), name='send email every 10s')