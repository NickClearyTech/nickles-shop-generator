from drf_spectacular.utils import extend_schema_field
from rest_framework import serializers
from django.contrib.auth.models import User
from gen.models import System, Item, Spell, Shop, SpellToShop, ItemToShop, Job


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ["password", "groups", "user_permissions"]


class UserSelfSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["username", "email"]


class SystemSerializer(serializers.ModelSerializer):
    class Meta:
        model = System
        fields = "__all__"


class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = "__all__"
        depth = 1

    system = serializers.SlugRelatedField(
        many=False, read_only=True, slug_field="abbreviation"
    )

    owner = serializers.SlugRelatedField(
        many=False, read_only=True, slug_field="username"
    )

    price = serializers.IntegerField(min_value=0)


class SpellSerializer(serializers.ModelSerializer):
    class Meta:
        model = Spell
        fields = "__all__"
        depth = 1

    system = serializers.SlugRelatedField(
        many=False, read_only=True, slug_field="abbreviation"
    )

    owner = serializers.SlugRelatedField(
        many=False, read_only=True, slug_field="username"
    )

    level = serializers.IntegerField(min_value=1, max_value=9)
    price = serializers.IntegerField(min_value=0)


class ItemShopSettings(serializers.Serializer):
    min_number = serializers.IntegerField(min_value=0, max_value=10000)
    max_number = serializers.IntegerField(min_value=0, max_value=10000)
    allow_duplicates = serializers.BooleanField(default=True)
    rarity = serializers.CharField(min_length=1, max_length=1)


class SpellShopSettings(serializers.Serializer):
    min_number = serializers.IntegerField(min_value=0, max_value=10000)
    max_number = serializers.IntegerField(min_value=0, max_value=10000)
    allow_duplicates = serializers.BooleanField(default=True)
    level = serializers.IntegerField(min_value=1, max_value=9)


class ShopSettingsSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=128, default="My New Shop")
    items = ItemShopSettings(many=True)
    spells = SpellShopSettings(many=True)

    def validate_items(self, value):
        rarities = ["C", "U", "R", "V", "L"]
        if len(value) != 5:
            raise serializers.ValidationError(
                "Invalid number of item settings, should be exactly 5"
            )
        for item_setting in value:
            if item_setting["rarity"].upper() in rarities:
                rarities.remove(item_setting["rarity"])
            else:
                raise serializers.ValidationError(
                    f"Multiple item settings have the same rarity, or invalid rarity specified: {item_setting['rarity']}"
                )
        return value

    def validate_spells(self, value):
        levels = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        if len(value) != 9:
            raise serializers.ValidationError(
                "Invalid number of spell settings, should be exactly 9"
            )
        for spell_setting in value:
            if spell_setting["level"] in levels:
                levels.remove(spell_setting["level"])
            else:
                raise serializers.ValidationError(
                    f"Multiple spell settings have the same level, or an invalid spell level was supplied: {spell_setting['level']}"
                )
        return value


class ShopToItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = ItemToShop
        exclude = ["id", "shop"]

    item = ItemSerializer()
    quantity = serializers.IntegerField(default=1)


class ShopToSpellSerializer(serializers.ModelSerializer):
    class Meta:
        model = SpellToShop
        exclude = ["id", "shop"]

    spell = SpellSerializer()
    quantity = serializers.IntegerField(default=1)


class ShopSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shop
        fields = "__all__"
        depth = 1

    owner = serializers.SlugRelatedField(slug_field="username", read_only=True)

    spells = serializers.SerializerMethodField("get_spells")
    items = serializers.SerializerMethodField("get_items")

    @extend_schema_field(
        {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "item": {"type": "string"},
                    "quantity": {"type": "integer"},
                },
            },
        }
    )
    def get_items(self, shop):
        item_queryset = ItemToShop.objects.filter(shop=shop)
        serializer = ShopToItemSerializer(
            instance=item_queryset, many=True, context=self.context
        )
        return serializer.data

    @extend_schema_field(
        {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "item": {"type": "string"},
                    "quantity": {"type": "integer"},
                },
            },
        }
    )
    def get_spells(self, shop):
        spell_queryset = SpellToShop.objects.filter(shop=shop)
        serializer = ShopToSpellSerializer(
            instance=spell_queryset, many=True, context=self.context
        )
        return serializer.data


class JobSerializer(serializers.ModelSerializer):
    class Meta:
        model = Job
        fields = "__all__"
        depth = 1

    job_parameters = serializers.DictField()
    job_result = serializers.DictField()
    launched_by = serializers.SlugRelatedField(slug_field="username", read_only=True)
