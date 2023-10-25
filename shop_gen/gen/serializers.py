from rest_framework import serializers
from django.contrib.auth.models import User
from gen.models import System, Item, Spell, Shop, SpellToShop, ItemToShop


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

    min_number = serializers.IntegerField(min_value=0)
    max_number = serializers.IntegerField(min_value=0)
    allow_duplicates = serializers.BooleanField(default=True)
    rarity = serializers.CharField(min_length=1, max_length=1)


class SpellShopSettings(serializers.Serializer):

    min_number = serializers.IntegerField(min_value=0)
    max_number = serializers.IntegerField(min_value=0)
    allow_duplicates = serializers.BooleanField(default=True)
    level = serializers.IntegerField(min_value=1, max_value=9)


class ShopSettingsSerializer(serializers.Serializer):

    name = serializers.CharField(max_length=128, default="My New Shop")
    items = ItemShopSettings(many=True)
    spells = SpellShopSettings(many=True)


class ShopToItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = ItemToShop
        exclude = ["pk"]

    shop = serializers.SlugRelatedField(
        many=True,
        slug_field="name",
        read_only=True
    )
    item = serializers.SlugRelatedField(
        many=True,
        slug_field="name",
        read_only=True
    )
    quantity = serializers.IntegerField(default=1)


class ShopToSpellSerializer(serializers.ModelSerializer):

    class Meta:
        model = SpellToShop
        exclude = ["pk"]

    shop = serializers.SlugRelatedField(
        many=True,
        slug_field="name",
        read_only=True
    )
    spell = serializers.SlugRelatedField(
        many=True,
        slug_field="name",
        read_only=True
    )
    quantity = serializers.IntegerField(default=1)


class ShopSerializer(serializers.ModelSerializer):

    class Meta:
        model = Shop
        fields = "__all__"
        depth = 1

    owner = UserSerializer()
    spells = serializers.ListField(
        child=ShopToSpellSerializer()
    )
    items = serializers.ListField(
        child=ShopToItemSerializer()
    )


