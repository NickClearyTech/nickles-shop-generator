from django.contrib.auth.models import User
from django.db import models


class DefaultFields(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    class Meta:
        abstract = True


class System(DefaultFields):
    abbreviation = models.CharField(max_length=8, null=False, default="NA")
    full_name = models.CharField(max_length=64, null=False, default="NA")


class ItemBase(DefaultFields):
    name = models.CharField(max_length=128, null=False)
    description = models.CharField(max_length=4096, null=True)
    system = models.ForeignKey(System, on_delete=models.CASCADE, null=False)
    price = models.IntegerField(default=0)
    public = models.BooleanField(db_index=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=True, db_index=True)
    sourcebook = models.CharField(null=True, max_length=32)

    class Meta:
        abstract = True


class Item(ItemBase):
    RARITY_CHOICES = [
        ("C", "Common"),
        ("U", "Uncommon"),
        ("R", "Rare"),
        ("V", "Very Rare"),
        ("L", "Legendary")
    ]
    magical = models.BooleanField(null=True, default=False)
    rarity = models.CharField(max_length=1, choices=RARITY_CHOICES, null=True)


class Spell(ItemBase):
    level = models.IntegerField(null=False)
