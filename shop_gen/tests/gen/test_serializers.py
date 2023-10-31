import pytest
from rest_framework import serializers

from gen.serializers import ShopSettingsSerializer
import copy

valid_serializer_data = {
    "items": [
        {"rarity": "C", "allow_duplicates": True, "min_number": 10, "max_number": 60},
        {"rarity": "U", "allow_duplicates": True, "min_number": 5, "max_number": 30},
        {"rarity": "R", "allow_duplicates": True, "min_number": 3, "max_number": 10},
        {"rarity": "V", "allow_duplicates": True, "min_number": 1, "max_number": 3},
        {"rarity": "L", "allow_duplicates": False, "min_number": 0, "max_number": 2},
    ],
    "spells": [
        {"level": 1, "allow_duplicates": True, "min_number": 20, "max_number": 50},
        {"level": 2, "allow_duplicates": True, "min_number": 20, "max_number": 50},
        {"level": 3, "allow_duplicates": True, "min_number": 20, "max_number": 50},
        {"level": 4, "allow_duplicates": True, "min_number": 20, "max_number": 50},
        {"level": 5, "allow_duplicates": True, "min_number": 20, "max_number": 50},
        {"level": 6, "allow_duplicates": True, "min_number": 20, "max_number": 50},
        {"level": 7, "allow_duplicates": True, "min_number": 20, "max_number": 50},
        {"level": 8, "allow_duplicates": True, "min_number": 20, "max_number": 50},
        {"level": 9, "allow_duplicates": True, "min_number": 20, "max_number": 50},
    ],
}


def test_valid_shop_generate_settings():
    shop_settings = ShopSettingsSerializer(data=valid_serializer_data)
    shop_settings.is_valid(raise_exception=True)
    assert shop_settings.data["name"] == "My New Shop"


def test_invalid_spell_level():
    test_data = copy.deepcopy(valid_serializer_data)
    test_data["spells"][0]["level"] = 30
    shop_settings = ShopSettingsSerializer(data=test_data)
    with pytest.raises(serializers.ValidationError):
        shop_settings.is_valid(raise_exception=True)


def test_duplicate_spell_level():
    test_data = copy.deepcopy(valid_serializer_data)
    test_data["spells"][0]["level"] = 2
    shop_settings = ShopSettingsSerializer(data=test_data)
    with pytest.raises(serializers.ValidationError):
        shop_settings.is_valid(raise_exception=True)


def test_too_few_spells():
    test_data = copy.deepcopy(valid_serializer_data)
    test_data["spells"] = test_data["spells"][1:5]
    shop_settings = ShopSettingsSerializer(data=test_data)
    with pytest.raises(serializers.ValidationError):
        shop_settings.is_valid(raise_exception=True)


def test_invalid_item_rarity():
    test_data = copy.deepcopy(valid_serializer_data)
    test_data["items"][0]["rarity"] = "N"
    shop_settings = ShopSettingsSerializer(data=test_data)
    with pytest.raises(serializers.ValidationError):
        shop_settings.is_valid(raise_exception=True)


def test_duplicate_item_rarity():
    test_data = copy.deepcopy(valid_serializer_data)
    test_data["items"][0]["rarity"] = "U"
    shop_settings = ShopSettingsSerializer(data=test_data)
    with pytest.raises(serializers.ValidationError):
        shop_settings.is_valid(raise_exception=True)


def test_too_few_items():
    test_data = copy.deepcopy(valid_serializer_data)
    test_data["items"] = test_data["items"][1:2]
    shop_settings = ShopSettingsSerializer(data=test_data)
    with pytest.raises(serializers.ValidationError):
        shop_settings.is_valid(raise_exception=True)
