from celery.exceptions import TaskError
from rest_framework.exceptions import ValidationError

from celery_settings import app as celery_app

from gen.models import Job
from gen.generator.generate_shop import generate_shop
from gen.serializers import ShopSettingsSerializer


def get_items_by_rarity(items, rarity):
    return items.filter(rarity=rarity).values_list("id", flat=True)


def get_spells_by_level(spells, level):
    return spells.filter(level=level).values_list("id", flat=True)


@celery_app.task(bind=True)
def generate_shop_task(self, job_id: int):
    if Job.objects.filter(id=job_id).count() != 1:
        raise TaskError("Invalid Job ID")
    job_object: Job = Job.objects.get(id=job_id)
    job_object.status = Job.Status.RUNNING
    job_object.save()

    serialized_data = ShopSettingsSerializer(data=job_object.job_parameters)

    try:
        serialized_data.is_valid(raise_exception=True)
    except ValidationError as e:
        job_object.status = Job.Status.FAILURE
        job_object.job_result = {"error": str(e)}
        job_object.save()
        return

    shop = generate_shop(serialized_data)

    job_object.job_result = {"shop_id": shop.id}
    job_object.status = Job.Status.COMPLETE
    job_object.save()

    return 0
