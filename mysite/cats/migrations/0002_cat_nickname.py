# Generated by Django 4.2.3 on 2024-03-31 00:12

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("cats", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="cat",
            name="nickname",
            field=models.CharField(
                default="Gato1",
                max_length=200,
                validators=[
                    django.core.validators.MinLengthValidator(
                        2, "Nickname must be greater than 1 character"
                    )
                ],
            ),
            preserve_default=False,
        ),
    ]