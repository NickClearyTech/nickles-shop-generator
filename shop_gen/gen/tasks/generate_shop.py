from celery.exceptions import TaskError

from celery_settings import app as celery_app

from gen.models import Job
from gen.querysets import get_items, get_spells


@celery_app.task(bind=True)
def generate_shop(self, job_id: int):
    if Job.objects.filter(id=job_id).count() != 1:
        raise TaskError("Invalid Job ID")
    job_object: Job = Job.objects.get(id=job_id)

    items = get_items(job_object.launched_by)
    spells = get_spells(job_object.launched_by)
    print(items.count())
    print(spells.count())
    return 0
