from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

from picklefield.fields import PickledObjectField


class DefaultFields(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    class Meta:
        abstract = True
        ordering = ["pk"]


class System(DefaultFields):
    abbreviation = models.CharField(max_length=8, null=False, default="NA")
    full_name = models.CharField(max_length=64, null=False, default="NA")

    class Meta:
        ordering = ["pk"]


class ItemBase(DefaultFields):
    name = models.CharField(max_length=128, null=False)
    description = models.CharField(max_length=4096, null=True)
    system = models.ForeignKey(
        System, on_delete=models.CASCADE, null=False, db_index=True
    )
    price = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    public = models.BooleanField(db_index=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=True, db_index=True)
    sourcebook = models.CharField(null=True, max_length=32, db_index=True)

    class Meta:
        abstract = True


class Item(ItemBase):
    RARITY_CHOICES = [
        ("C", "Common"),
        ("U", "Uncommon"),
        ("R", "Rare"),
        ("V", "Very Rare"),
        ("L", "Legendary"),
    ]
    magical = models.BooleanField(null=True, default=False)
    rarity = models.CharField(max_length=1, choices=RARITY_CHOICES, null=True)

    class Meta:
        ordering = ["pk"]
        constraints = [
            models.UniqueConstraint(
                fields=("name", "owner", "system"),
                name="unique_name_per_owner_system_item",
            )
        ]


class Spell(ItemBase):
    level = models.IntegerField(
        null=False, validators=[MinValueValidator(1), MaxValueValidator(9)]
    )

    class Meta:
        ordering = ["pk"]
        constraints = [
            models.UniqueConstraint(
                fields=("name", "owner", "system"),
                name="unique_name_per_owner_system_spell",
            )
        ]


class ItemToShop(models.Model):
    item = models.ForeignKey(to=Item, on_delete=models.CASCADE)
    shop = models.ForeignKey(to="Shop", on_delete=models.CASCADE)
    quantity = models.IntegerField(
        null=False, default=1, validators=[MinValueValidator(0)]
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=("item", "shop"), name="once_per_shop_item")
        ]
        ordering = ["pk"]


class SpellToShop(models.Model):
    spell = models.ForeignKey(to=Spell, on_delete=models.CASCADE)
    shop = models.ForeignKey(to="Shop", on_delete=models.CASCADE)
    quantity = models.IntegerField(
        null=False, default=1, validators=[MinValueValidator(0)]
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=("spell", "shop"), name="once_per_shop_spell"
            )
        ]
        indexes = [models.Index("spell", "shop", name="spell_shop_composite_index")]


class ShopWarning(DefaultFields):
    error = models.BooleanField(default=False)
    note = models.CharField(max_length=512)
    shop = models.ForeignKey("Shop", related_name="warnings", on_delete=models.CASCADE)


class Shop(DefaultFields):
    items = models.ManyToManyField(to=Item, through=ItemToShop)
    spells = models.ManyToManyField(to=Spell, through=SpellToShop)
    owner = models.ForeignKey(
        to=User, on_delete=models.CASCADE, null=True, db_index=True
    )
    name = models.CharField(max_length=128, null=False, default="My New Shop")

    class Meta:
        ordering = ["pk"]


class Job(DefaultFields):
    class Status(models.TextChoices):
        RECEIVED = "Received"
        RUNNING = "Running"
        COMPLETE = "Complete"
        FAILURE = "Failure"
        CANCELLED = "Cancelled"

    class JobType(models.TextChoices):
        GENERATE_SHOP = "Generate Shop"
        IMPORT_FOUNDRY_ITEMS = "Import Foundry Items"

    status = models.CharField(
        max_length=32, choices=Status.choices, default=Status.RECEIVED, db_index=True
    )
    job_type = models.CharField(max_length=32, choices=JobType.choices, db_index=True)
    launched_by = models.ForeignKey(
        to=User, on_delete=models.CASCADE, null=False, db_index=True
    )
    job_parameters = PickledObjectField(null=False)
    job_result = PickledObjectField(null=True)
