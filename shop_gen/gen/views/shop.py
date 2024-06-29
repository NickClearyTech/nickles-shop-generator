from django.template.response import TemplateResponse

from gen.models import Shop, Item, ItemToShop, SpellToShop
from gen.lookups import ItemType

import logging

logger = logging.getLogger(__name__)


def shop_detail(request, id):
    shop = Shop.objects.prefetch_related("items").get(id=id)
    logger.warning("shop_detail called")
    item_to_shops = (
        ItemToShop.objects.select_related("item", "item__sourcebook")
        .filter(shop=shop)
        .all()
    )

    spell_to_shops = (
        SpellToShop.objects.select_related("spell", "spell__sourcebook")
        .filter(shop=shop)
        .all()
    )

    items_dict = {"equipment": [], "magic_items": [], "potions": [], "spells": []}

    for item in item_to_shops:
        # Potions
        if item.item.type == ItemType.POTION:
            items_dict["potions"].append({"quantity": item.quantity, "item": item.item})
        # Magical items
        elif (
            item.item.type
            in [
                ItemType.SCROLL,
                ItemType.WAND,
                ItemType.SPELLCASTING_FOCUS,
                ItemType.MASTER_RUNE,
                ItemType.RG,
            ]
            or item.item.magical
        ):
            items_dict["magic_items"].append(
                {"quantity": item.quantity, "item": item.item}
            )
        # If not equipment or potion, assume its a magical item
        else:
            items_dict["equipment"].append(
                {"quantity": item.quantity, "item": item.item}
            )

    spells = []
    for spell in spell_to_shops:
        spells.append({"quantity": spell.quantity, "spell": spell.spell})

    return TemplateResponse(
        request,
        "single_shop.html",
        {"shop": shop, "items": items_dict, "spells": spells},
    )
