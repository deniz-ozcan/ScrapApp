# Generated by Django 4.1.2 on 2022-10-19 14:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("scrap", "0017_sitesinformation_sitename"),
    ]

    operations = [
        migrations.AddField(
            model_name="product",
            name="sitelink",
            field=models.CharField(blank=True, max_length=250, null=True),
        ),
    ]
