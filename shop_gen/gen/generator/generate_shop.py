from random import randint, sample, choices
from typing import Callable, List

from gen.serializers import ShopSettingsSerializer
from gen.models import Shop, ShopWarning, ItemToShop, Item, SpellToShop, Spell
from gen.querysets.item_queries import (
    get_potions,
    get_equipment,
    get_magic_items,
    get_spells_by_level,
)

from logging import getLogger

logger = getLogger(__name__)


def get_settings_by_rarity(shop_settings_list, rarity, is_spell: bool = False):
    """
    A helper method that gets from the shop settings the setting of a particular rarity
    """
    for shop_settings in shop_settings_list:
        if (not is_spell and shop_settings.get("rarity") == rarity) or (
            is_spell and shop_settings.get("level") == rarity
        ):
            return shop_settings


def generate_items_of_type(
    shop_object: Shop, shop_settings, item_type: str, get_item_function: Callable
):
    shop_to_item_list: List[ItemToShop] = []

    for rarity in ["V", "C", "U", "R", "L"]:
        logger.info(
            f"Generating {item_type} items for rarity {rarity} for shop #{shop_object.id}"
        )
        rarity_settings = get_settings_by_rarity(shop_settings[item_type], rarity)
        if rarity_settings["min_number"] == 0 and rarity_settings["max_number"] == 0:
            # If none of this rarity are required, continue
            continue
        item_ids = get_item_function(rarity)

        rarity_number: int = randint(
            rarity_settings["min_number"], rarity_settings["max_number"]
        )

        selected_item_ids: List[int] = []

        # When no replacement
        if not rarity_settings["allow_duplicates"]:
            # If the selected number of items is more than the possible number of items
            if rarity_number > len(item_ids):
                # Set the number of items to select to the maximum possible
                rarity_number = len(item_ids)

                # Create a warning object
                warning: ShopWarning = ShopWarning()
                warning.shop = shop_object
                warning.error = False
                warning.note = f"The randomly selected number of items for rarity {rarity['rarity']} was more than the available number of of items ({len(item_ids)}). Selecting {len(item_ids)} items."
                warning.save()

            selected_item_ids += sample(item_ids, rarity_number)
        else:
            selected_item_ids += choices(item_ids, k=rarity_number)

        id_to_quantity = {}

        for id in selected_item_ids:
            if id not in id_to_quantity.keys():
                id_to_quantity[id] = 1
            else:
                id_to_quantity[id] += 1

        for id, quantity in id_to_quantity.items():
            shop_to_item = ItemToShop()
            shop_to_item.shop = shop_object
            shop_to_item.item = Item.objects.get(id=id)
            shop_to_item.quantity = quantity
            shop_to_item_list.append(shop_to_item)

    ItemToShop.objects.bulk_create(shop_to_item_list)


def generate_shop_spells(shop_object: Shop, shop_settings):
    shop_to_spell_list: List[SpellToShop] = []

    for level in range(0, 10):
        logger.info(f"Generating spells for level {level} for shop #{shop_object.id}")
        level_settings = get_settings_by_rarity(
            shop_settings["spells"], level, is_spell=True
        )
        if level_settings["min_number"] == 0 and level_settings["max_number"] == 0:
            # If none of this level are required, continue
            continue

        spell_ids = get_spells_by_level(level)

        rarity_number: int = randint(
            level_settings["min_number"], level_settings["max_number"]
        )

        selected_spell_ids: List[int] = []

        # When no replacement
        if not level_settings["allow_duplicates"]:
            # If the selected number of items is more than the possible number of items
            if rarity_number > len(spell_ids):
                # Set the number of items to select to the maximum possible
                rarity_number = len(spell_ids)

                # Create a warning object
                warning: ShopWarning = ShopWarning()
                warning.shop = shop_object
                warning.error = False
                warning.note = f"The randomly selected number of spells for level {level} was more than the available number of of items ({len(spell_ids)}). Selecting {len(spell_ids)} items."
                warning.save()

            selected_spell_ids += sample(spell_ids, rarity_number)
        else:
            selected_spell_ids += choices(spell_ids, k=rarity_number)

        id_to_quantity = {}

        for id in selected_spell_ids:
            if id not in id_to_quantity.keys():
                id_to_quantity[id] = 1
            else:
                id_to_quantity[id] += 1

        for id, quantity in id_to_quantity.items():
            shop_to_spell = SpellToShop()
            shop_to_spell.shop = shop_object
            shop_to_spell.spell = Spell.objects.get(id=id)
            shop_to_spell.quantity = quantity
            shop_to_spell_list.append(shop_to_spell)

    SpellToShop.objects.bulk_create(shop_to_spell_list)


def generate_shop(settings: ShopSettingsSerializer) -> Shop:

    shop: Shop = Shop()
    shop.owner = None
    shop.name = settings.data["name"]
    shop.save()

    logger.info(f"Generating shop with name {shop.name} and ID {shop.id}")

    generate_items_of_type(shop, settings.data, "potions", get_potions)
    generate_items_of_type(shop, settings.data, "equipment", get_equipment)
    generate_items_of_type(shop, settings.data, "magical_items", get_magic_items)
    generate_shop_spells(shop, settings.data)

    logger.info(f"Finished generating shop {shop.id}")
    return shop
