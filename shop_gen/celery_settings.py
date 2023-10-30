import os

from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")

app = Celery("gen", include=["gen.tasks.generate_shop"])

app.config_from_object("django.conf:settings")
app.worker_prefetch_multiplier = 2
app.task_acks_late = True

app.autodiscover_tasks()
