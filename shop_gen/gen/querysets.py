from rest_framework.request import Request
from django.db.models import Q

from gen.models import Item, Spell


def get_items(user):
    if user.is_superuser:
        return Item.objects.all()
    return Item.objects.filter(Q(public=True) | Q(owner=user))


def get_spells(user):
    if user.is_superuser:
        return Spell.objects.all()
    return Spell.objects.filter(Q(public=True) | Q(owner=user))
