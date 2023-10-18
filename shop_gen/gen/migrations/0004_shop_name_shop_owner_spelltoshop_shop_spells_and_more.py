# Generated by Django 4.2.6 on 2023-10-17 13:57

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("gen", "0003_itemtoshop_shop_itemtoshop_shop_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="shop",
            name="name",
            field=models.CharField(default="My New Shop", max_length=128),
        ),
        migrations.AddField(
            model_name="shop",
            name="owner",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.CreateModel(
            name="SpellToShop",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("quantity", models.IntegerField(default=1)),
                (
                    "shop",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="gen.shop"
                    ),
                ),
                (
                    "spell",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="gen.spell"
                    ),
                ),
            ],
        ),
        migrations.AddField(
            model_name="shop",
            name="spells",
            field=models.ManyToManyField(through="gen.SpellToShop", to="gen.spell"),
        ),
        migrations.AddConstraint(
            model_name="spelltoshop",
            constraint=models.UniqueConstraint(
                fields=("spell", "shop"), name="once_per_shop_spell"
            ),
        ),
    ]
