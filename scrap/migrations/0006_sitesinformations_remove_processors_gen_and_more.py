# Generated by Django 4.1.2 on 2022-10-18 02:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("scrap", "0005_remove_product_protype_processors_type_and_more"),
    ]

    operations = [
        migrations.CreateModel(
            name="SitesInformations",
            fields=[
                (
                    "_id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=100)),
                ("link", models.URLField()),
                (
                    "rate",
                    models.DecimalField(decimal_places=0, default=0, max_digits=1),
                ),
                ("price", models.DecimalField(decimal_places=2, max_digits=6)),
            ],
        ),
        migrations.RemoveField(
            model_name="processors",
            name="gen",
        ),
        migrations.RemoveField(
            model_name="product",
            name="hepsiburada",
        ),
        migrations.RemoveField(
            model_name="product",
            name="n11",
        ),
        migrations.RemoveField(
            model_name="product",
            name="name",
        ),
        migrations.RemoveField(
            model_name="product",
            name="trendyol",
        ),
        migrations.RemoveField(
            model_name="product",
            name="vatan",
        ),
        migrations.AddField(
            model_name="product",
            name="title",
            field=models.CharField(blank=True, max_length=250, null=True, unique=True),
        ),
        migrations.AlterField(
            model_name="rams",
            name="type",
            field=models.CharField(max_length=5),
        ),
        migrations.AlterField(
            model_name="storages",
            name="type",
            field=models.CharField(max_length=5),
        ),
        migrations.DeleteModel(
            name="Brands",
        ),
        migrations.DeleteModel(
            name="Hepsiburada",
        ),
        migrations.DeleteModel(
            name="N11",
        ),
        migrations.DeleteModel(
            name="Trendyol",
        ),
        migrations.DeleteModel(
            name="Vatan",
        ),
        migrations.AddField(
            model_name="product",
            name="sites",
            field=models.ManyToManyField(blank=True, to="scrap.sitesinformations"),
        ),
    ]
