import random
from random import randint
from typing import List

from celery.exceptions import TaskError

from celery_settings import app as celery_app

from gen.models import Job, Shop, ItemToShop, Item, ShopWarning, SpellToShop, Spell
from gen.querysets import get_items, get_spells


def get_items_by_rarity(items, rarity):
    return items.filter(rarity=rarity).values_list("id", flat=True)


def get_spells_by_level(spells, level):
    return spells.filter(level=level).values_list("id", flat=True)


@celery_app.task(bind=True)
def generate_shop(self, job_id: int):
    if Job.objects.filter(id=job_id).count() != 1:
        raise TaskError("Invalid Job ID")
    job_object: Job = Job.objects.get(id=job_id)
    job_object.status = Job.Status.RUNNING
    job_object.save()

    print(f"Processing job with ID {job_id}")

    items = get_items(job_object.launched_by)
    spells = get_spells(job_object.launched_by)

    shop: Shop = Shop()
    shop.owner = job_object.launched_by
    shop.name = job_object.job_parameters["name"]
    shop.save()

    # Generate items

    selected_item_ids: List[int] = []

    for item_settings in job_object.job_parameters["items"]:
        print(f"Getting items with rarity {item_settings['rarity']}")
        rarity_item_ids = list(get_items_by_rarity(items, item_settings["rarity"]))
        rarity_number: int = randint(
            item_settings["min_number"], item_settings["max_number"]
        )

        # When no replacement
        if not item_settings["allow_duplicates"]:
            # If the selected number of items is more than the possible number of items
            if rarity_number > len(rarity_item_ids):
                # Set the number of items to select to the maximum possible
                rarity_number = len(rarity_item_ids)

                # Create a warning object
                warning: ShopWarning = ShopWarning()
                warning.shop = shop
                warning.error = False
                warning.note = f"The randomly selected number of items for rarity {item_settings['rarity']} was more than the available number of of items ({len(rarity_item_ids)}). Selecting {len(rarity_item_ids)} items."
                warning.save()

            selected_item_ids += random.sample(rarity_item_ids, rarity_number)
        else:
            selected_item_ids += random.choices(rarity_item_ids, k=rarity_number)

    id_to_quantity = {}

    for id in selected_item_ids:
        if id not in id_to_quantity.keys():
            id_to_quantity[id] = 1
        else:
            id_to_quantity[id] += 1

    shop_to_item_list: List[ItemToShop] = []
    for id, quantity in id_to_quantity.items():
        shop_to_item = ItemToShop()
        shop_to_item.shop = shop
        shop_to_item.item = Item.objects.get(id=id)
        shop_to_item.quantity = quantity
        shop_to_item_list.append(shop_to_item)

    ItemToShop.objects.bulk_create(shop_to_item_list)

    # Generate spells
    selected_spell_ids: List[int] = []

    # for spell_settings in job_object.job_parameters["spells"]:
    #     print(f"Getting spells with level {spell_settings['level']}")
    #     level_spell_ids: List[int] = list(get_spells_by_level(spells, spell_settings['level']))
    #     level_number: int = randint(
    #         spell_settings["min_number"], spell_settings["max_number"]
    #     )
    #
    #     if not spell_settings["allow_duplicates"]:
    #         # if the selected number of spells is more than the possible number of spells
    #         if level_number > len(level_spell_ids):
    #             # Set number of spells to the maximum possible
    #             level_number = len(level_spell_ids)
    #             # Create a warning object
    #             warning: ShopWarning = ShopWarning()
    #             warning.shop = shop
    #             warning.error = False
    #             warning.note = f"The randomly selected number of spells for level {spell_settings['level']} was more than the available number of of spells ({len(level_spell_ids)}). Selecting {len(level_spell_ids)} items."
    #             warning.save()
    #
    #             selected_spell_ids += random.sample(level_spell_ids, level_number)
    #     else:
    #         print(level_number)
    #         selected_spell_ids += random.choices(level_spell_ids, k=level_number)
    #
    # id_to_quantity = {}
    # for id in selected_spell_ids:
    #     if id not in id_to_quantity.keys():
    #         id_to_quantity[id] = 1
    #     else:
    #         id_to_quantity[id] += 1
    #
    # shop_to_spell_list: List[SpellToShop] = []
    # for id, quantity in id_to_quantity.items():
    #     shop_to_spell = SpellToShop()
    #     shop_to_spell.shop = shop
    #     shop_to_spell.spell = Spell.objects.get(id=id)
    #     shop_to_spell.quantity = quantity
    #     shop_to_spell_list.append(shop_to_spell)
    #
    # SpellToShop.objects.bulk_create(shop_to_spell_list)

    shop.save()

    job_object.job_result = {
        "shop_id": shop.id
    }
    job_object.status = Job.Status.COMPLETE
    job_object.save()

    return 0
