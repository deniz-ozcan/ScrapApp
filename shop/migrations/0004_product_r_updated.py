# Generated by Django 4.1.2 on 2022-10-23 10:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0003_alter_brand_model_alter_brand_name_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='r_updated',
            field=models.DateTimeField(auto_now=True, null=True, verbose_name='Updated'),
        ),
    ]