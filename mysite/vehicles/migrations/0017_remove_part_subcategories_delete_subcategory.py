# Generated by Django 4.2.7 on 2024-07-05 13:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('vehicles', '0016_part_sku'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='part',
            name='subcategories',
        ),
        migrations.DeleteModel(
            name='SubCategory',
        ),
    ]