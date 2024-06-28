from django.template.response import TemplateResponse

from gen.models import Shop, Item, ItemToShop

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
    items = []
    for item in item_to_shops:
        items.append({"quantity": item.quantity, "item": item.item})

    # for item in shop_items:
    #     print(item.item.id)
    # items = Item.objects.filter(id__in=ids)
    return TemplateResponse(request, "single_shop.html", {"shop": shop, "items": items})
