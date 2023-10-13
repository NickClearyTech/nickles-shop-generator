from django.contrib.auth.models import User
from django.db import models


class System(models.Model):
    abbreviation = models.CharField(max_length=8, null=False, default="NA")
    full_name = models.CharField(max_length=64, null=False, default="NA")


class Item(models.Model):
    RARITY_CHOICES = [
        ("C", "Common"),
        ("U", "Uncommon"),
        ("R", "Rare"),
        ("V", "Very Rare"),
        ("L", "Legendary")
    ]

    name = models.CharField(max_length=128, null=False)
    description = models.CharField(max_length=4096, null=True)
    system = models.ForeignKey(System, on_delete=models.CASCADE, null=False)
    price = models.IntegerField(default=0)
    public = models.BooleanField(db_index=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=True, db_index=True)
    magical = models.BooleanField(null=True, default=False)
    rarity = models.CharField(max_length=1, choices=RARITY_CHOICES, null=True)
