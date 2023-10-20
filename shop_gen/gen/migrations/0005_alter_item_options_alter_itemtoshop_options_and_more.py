# Generated by Django 4.2.6 on 2023-10-20 02:07

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("gen", "0004_shop_name_shop_owner_spelltoshop_shop_spells_and_more"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="item",
            options={"ordering": ["pk"]},
        ),
        migrations.AlterModelOptions(
            name="itemtoshop",
            options={"ordering": ["pk"]},
        ),
        migrations.AlterModelOptions(
            name="shop",
            options={"ordering": ["pk"]},
        ),
        migrations.AlterModelOptions(
            name="spell",
            options={"ordering": ["pk"]},
        ),
        migrations.AlterModelOptions(
            name="system",
            options={"ordering": ["pk"]},
        ),
        migrations.AlterField(
            model_name="item",
            name="price",
            field=models.IntegerField(
                default=0, validators=[django.core.validators.MinValueValidator(0)]
            ),
        ),
        migrations.AlterField(
            model_name="item",
            name="sourcebook",
            field=models.CharField(db_index=True, max_length=32, null=True),
        ),
        migrations.AlterField(
            model_name="itemtoshop",
            name="quantity",
            field=models.IntegerField(
                default=1, validators=[django.core.validators.MinValueValidator(0)]
            ),
        ),
        migrations.AlterField(
            model_name="spell",
            name="level",
            field=models.IntegerField(
                validators=[
                    django.core.validators.MinValueValidator(1),
                    django.core.validators.MaxValueValidator(9),
                ]
            ),
        ),
        migrations.AlterField(
            model_name="spell",
            name="price",
            field=models.IntegerField(
                default=0, validators=[django.core.validators.MinValueValidator(0)]
            ),
        ),
        migrations.AlterField(
            model_name="spell",
            name="sourcebook",
            field=models.CharField(db_index=True, max_length=32, null=True),
        ),
        migrations.AlterField(
            model_name="spelltoshop",
            name="quantity",
            field=models.IntegerField(
                default=1, validators=[django.core.validators.MinValueValidator(0)]
            ),
        ),
    ]
