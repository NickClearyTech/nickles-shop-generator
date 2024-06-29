from django.db.models import Q

from gen.models import Item, Spell
from gen.lookups import ItemType


def get_equipment(rarity: str):
    return (
        Item.objects.filter(
            type__in=[
                ItemType.AMMUNITION,
                ItemType.AMMO,
                ItemType.ARTISANS_TOOLS,
                ItemType.EXPLOSIVE,
                ItemType.FOOD_AND_DRINK,
                ItemType.ADVENTURING_GEAR,
                ItemType.GAMING_SET,
                ItemType.HEAVY_ARMOR,
                ItemType.ILLEGAL_DRUG,
                ItemType.INSTRUMENT,
                ItemType.LARGE_ARMOR,
                ItemType.MELEE_WEAPON,
                ItemType.MEDIUM_ARMOR,
                ItemType.MOUNT,
                ItemType.GENERIC_VARIANT,
                ItemType.SHIELD,
                ItemType.TOOL,
                ItemType.OTHER,
                ItemType.TACK_AND_HARNESS,
                ItemType.TRADE_GOOD,
                ItemType.RANGED_WEAPON,
                ItemType.TREASURE,
                ItemType.TREASURE_COINAGE,
                ItemType.TREASURE_COINAGE,
            ],
            rarity=rarity,
            magical=False,
        )
        .values_list("id", flat=True)
        .all()
    )


def get_potions(rarity: str):
    return (
        Item.objects.filter(type=ItemType.POTION, rarity=rarity, magical=False)
        .values_list("id", flat=True)
        .all()
    )


def get_items(user):
    if user.is_superuser:
        return Item.objects.all()
    return Item.objects.filter(Q(public=True) | Q(owner=user))


def get_magic_items(rarity: str):
    return (
        Item.objects.filter(
            (
                Q(
                    type__in=[
                        ItemType.SCROLL,
                        ItemType.WAND,
                        ItemType.SPELLCASTING_FOCUS,
                        ItemType.MASTER_RUNE,
                        ItemType.RG,
                    ]
                )
                | Q(magical=True)
            )
            & Q(rarity=rarity)
        )
        .values_list("id", flat=True)
        .all()
    )


def get_spells_by_level(level: int):
    return Spell.objects.filter(level=level).values_list("id", flat=True).all()


def get_spells(user):
    if user.is_superuser:
        return Spell.objects.all()
    return Spell.objects.filter(Q(public=True) | Q(owner=user))
