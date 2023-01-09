# Generated by Django 4.1.2 on 2022-10-18 03:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("scrap", "0008_alter_product_ram_alter_product_screen_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="product",
            name="sites",
        ),
        migrations.AddField(
            model_name="sitesinformation",
            name="whichproduct",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="scrap.product",
                verbose_name="Screen",
            ),
        ),
        migrations.AlterField(
            model_name="sitesinformation",
            name="name",
            field=models.CharField(blank=True, max_length=250, null=True, unique=True),
        ),
    ]
