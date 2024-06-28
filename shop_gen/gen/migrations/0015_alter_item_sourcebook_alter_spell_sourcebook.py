# Generated by Django 4.2.7 on 2024-05-12 18:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("gen", "0014_alter_book_abbreviation"),
    ]

    operations = [
        migrations.AlterField(
            model_name="item",
            name="sourcebook",
            field=models.ForeignKey(
                null=True, on_delete=django.db.models.deletion.CASCADE, to="gen.book"
            ),
        ),
        migrations.AlterField(
            model_name="spell",
            name="sourcebook",
            field=models.ForeignKey(
                null=True, on_delete=django.db.models.deletion.CASCADE, to="gen.book"
            ),
        ),
    ]