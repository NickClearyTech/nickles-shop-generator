from drf_spectacular.utils import extend_schema_field
from rest_framework import serializers
from django.contrib.auth.models import User
from gen.models import System, Item, Spell, Shop, SpellToShop, ItemToShop, Job, Book
from gen.consts import ITEM_RARITY_CODES


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


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
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

    def validate_rarity(self, value):
        if value not in ITEM_RARITY_CODES:
            raise serializers.ValidationError(
                "Rarity must be one of: {}".format(ITEM_RARITY_CODES)
            )
        return value


class SpellShopSettings(serializers.Serializer):
    min_number = serializers.IntegerField(min_value=0, max_value=10000)
    max_number = serializers.IntegerField(min_value=0, max_value=10000)
    allow_duplicates = serializers.BooleanField(default=True)
    level = serializers.IntegerField(min_value=0, max_value=9)


class ShopSettingsSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=128, default="My New Shop")
    magical_items = ItemShopSettings(many=True, required=False)
    equipment = ItemShopSettings(many=True, required=False)
    potions = ItemShopSettings(many=True, required=False)
    spells = SpellShopSettings(many=True, required=False)

    def run_item_validation(self, value, field_name: str):
        rarities = ["C", "U", "R", "V", "L"]
        if len(value) != len(rarities):
            raise serializers.ValidationError(
                f"Invalid number of {field_name} settings, should be exactly 5"
            )
        for item_setting in value:
            if item_setting["rarity"].upper() in rarities:
                rarities.remove(item_setting["rarity"])
            else:
                raise serializers.ValidationError(
                    f"Multiple {field_name} settings have the same rarity, or invalid rarity specified: {item_setting['rarity']}"
                )
        return value

    def validate_magical_items(self, value):
        return self.run_item_validation(value, "magical_items")

    def validate_equipment(self, value):
        return self.run_item_validation(value, "equipment")

    def validate_potions(self, value):
        return self.run_item_validation(value, "potions")

    def validate_spells(self, value):
        levels = list(range(0, 10))
        if len(value) != len(levels):
            raise serializers.ValidationError(
                "Invalid number of spell settings, should be exactly 10"
            )
        for spell_setting in value:
            if spell_setting["level"] in levels:
                levels.remove(spell_setting["level"])
            else:
                raise serializers.ValidationError(
                    f"Multiple spell settings have the same level, or an invalid spell level was supplied: {spell_setting['level']}"
                )
        return value

    def validate(self, data):
        if (
            (data["equipment"] is None or len(data["equipment"]) == 0)
            and (data["magical_items"] is None or len(data["magical_items"]) == 0)
            and (data["potions"] is None or len(data["potions"]) == 0)
            and (data["spells"] is None or len(data["spells"]) == 0)
        ):
            raise serializers.ValidationError(
                "At least one type of item or spell must be for sale!"
            )
        return data


class ShopToItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = ItemToShop
        exclude = ["id", "shop"]

    item = serializers.SlugRelatedField(slug_field="id", read_only=True)
    quantity = serializers.IntegerField(default=1)


class ShopToSpellSerializer(serializers.ModelSerializer):
    class Meta:
        model = SpellToShop
        exclude = ["id", "shop"]

    spell = serializers.SlugRelatedField(slug_field="id", read_only=True)
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
