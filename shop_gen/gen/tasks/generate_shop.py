from celery.exceptions import TaskError

from celery_settings import app as celery_app

from gen.models import Job


@celery_app.task(bind=True)
def generate_shop(self, job_id: int):
    if Job.objects.filter(id=job_id).count() != 1:
        raise TaskError("Invalid Job ID")
    job_object: Job = Job.objects.get(id=job_id)

    print(type(self))
    print("Job successful")
    return 0
