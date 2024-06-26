import pytest
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User

from gen.models import System, Item, Spell, Book


@pytest.mark.django_db
def test_min_item_price():
    item: Item = Item(
        **{
            "name": "test name",
            "description": "A test desc",
            "price": -1,
            "public": True,
            "sourcebook": Book.objects.get(id=2),
            "magical": True,
            "rarity": "C",
        }
    )
    item.owner = User.objects.create()
    item.system = System.objects.get(abbreviation="DnD5e")
    with pytest.raises(ValidationError):
        item.full_clean()


@pytest.mark.django_db
def test_min_spell_level():
    spell: Spell = Spell(
        **{
            "name": "test name",
            "description": "A test desc",
            "price": 50,
            "public": True,
            "sourcebook": Book.objects.get(id=2),
            "level": -1,
        }
    )
    spell.owner = User.objects.create()
    spell.system = System.objects.get(abbreviation="DnD5e")
    with pytest.raises(ValidationError):
        spell.full_clean()
    try:
        spell.full_clean()
    except ValidationError as e:
        assert len(e.message_dict) == 1


@pytest.mark.django_db
def test_max_spell_level():
    spell: Spell = Spell(
        **{
            "name": "test name",
            "description": "A test desc",
            "price": 50,
            "public": True,
            "sourcebook": Book.objects.get(id=2),
            "level": 10,
        }
    )
    spell.owner = User.objects.create()
    spell.system = System.objects.get(abbreviation="DnD5e")
    with pytest.raises(ValidationError):
        spell.full_clean()
    try:
        spell.full_clean()
    except ValidationError as e:
        assert len(e.message_dict) == 1
