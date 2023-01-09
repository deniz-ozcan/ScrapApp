# Generated by Django 4.1.2 on 2022-10-18 04:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("scrap", "0013_alter_sitesinformation_price_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="sitesinformation",
            name="whichproduct",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="scrap.product",
                verbose_name="Laptop",
            ),
        ),
    ]
