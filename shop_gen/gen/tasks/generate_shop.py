import random
from random import randint
from typing import List

from celery.exceptions import TaskError

from celery_settings import app as celery_app

from gen.models import Job, Shop, ItemToShop, Item
from gen.querysets import get_items, get_spells


def get_items_by_rarity(items, rarity):
    return items.filter(rarity=rarity).values_list("id", flat=True)


@celery_app.task(bind=True)
def generate_shop(self, job_id: int):
    if Job.objects.filter(id=job_id).count() != 1:
        raise TaskError("Invalid Job ID")
    job_object: Job = Job.objects.get(id=job_id)

    print(f"Processing job with ID {job_id}")

    items = get_items(job_object.launched_by)
    spells = get_spells(job_object.launched_by)

    selected_item_ids: List[int] = []

    for item_settings in job_object.job_parameters["items"]:
        print(f"Getting items with rarity {item_settings['rarity']}")
        rarity_item_ids = list(get_items_by_rarity(items, item_settings['rarity']))
        rarity_number: List[int] = randint(item_settings["min_number"], item_settings["max_number"])

        selected: List[int] = None

        # When no replacement
        if not item_settings["allow_duplicates"]:
            selected = random.choices(rarity_item_ids, k=rarity_number)
        else:
            selected = random.sample(rarity_item_ids, rarity_number)

        selected_item_ids += selected

    print(selected_item_ids)

    shop: Shop = Shop()
    shop.owner = job_object.launched_by
    shop.name = job_object.job_parameters["name"]
    shop.save()

    id_to_quantity = {}

    for id in selected_item_ids:
        if id not in id_to_quantity.keys():
            id_to_quantity[id] = 1
        else:
            id_to_quantity[id] += 1

    for id, quantity in id_to_quantity.items():
        shop_to_item = ItemToShop()
        shop_to_item.shop = shop
        shop_to_item.item = Item.objects.get(id=id)
        shop_to_item.quantity = quantity
        shop_to_item.save()

    shop.save()

    return 0
