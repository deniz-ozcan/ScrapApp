# Generated by Django 4.1.2 on 2022-10-17 23:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("scrap", "0002_protype_remove_processors_type_products_protype"),
    ]

    operations = [
        migrations.CreateModel(
            name="Hepsiburada",
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
                ("link", models.URLField()),
                (
                    "rate",
                    models.DecimalField(decimal_places=0, default=0, max_digits=1),
                ),
                ("price", models.DecimalField(decimal_places=2, max_digits=6)),
            ],
        ),
        migrations.CreateModel(
            name="N11",
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
                ("link", models.URLField()),
                (
                    "rate",
                    models.DecimalField(decimal_places=0, default=0, max_digits=1),
                ),
                ("price", models.DecimalField(decimal_places=2, max_digits=6)),
            ],
        ),
        migrations.CreateModel(
            name="Trendyol",
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
                ("link", models.URLField()),
                (
                    "rate",
                    models.DecimalField(decimal_places=0, default=0, max_digits=1),
                ),
                ("price", models.DecimalField(decimal_places=2, max_digits=6)),
            ],
        ),
        migrations.CreateModel(
            name="Vatan",
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
                ("link", models.URLField()),
                (
                    "rate",
                    models.DecimalField(decimal_places=0, default=0, max_digits=1),
                ),
                ("price", models.DecimalField(decimal_places=2, max_digits=6)),
            ],
        ),
        migrations.RemoveField(
            model_name="products",
            name="sites",
        ),
        migrations.DeleteModel(
            name="Sites",
        ),
        migrations.AddField(
            model_name="products",
            name="hepsiburada",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="scrap.hepsiburada",
                verbose_name="Hepsiburada",
            ),
        ),
        migrations.AddField(
            model_name="products",
            name="n11",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="scrap.n11",
                verbose_name="N11",
            ),
        ),
        migrations.AddField(
            model_name="products",
            name="trendyol",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="scrap.trendyol",
                verbose_name="Trendyol",
            ),
        ),
        migrations.AddField(
            model_name="products",
            name="vatan",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="scrap.vatan",
                verbose_name="Vatan",
            ),
        ),
    ]