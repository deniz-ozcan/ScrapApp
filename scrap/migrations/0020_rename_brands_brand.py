# Generated by Django 4.1.2 on 2022-10-20 13:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("scrap", "0019_rename_sitelink_product_image"),
    ]

    operations = [
        migrations.RenameModel(
            old_name="Brands",
            new_name="Brand",
        ),
    ]
