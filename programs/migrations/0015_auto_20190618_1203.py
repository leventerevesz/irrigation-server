# Generated by Django 2.2.2 on 2019-06-18 12:03

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('programs', '0014_auto_20190617_2115'),
    ]

    operations = [
        migrations.AlterField(
            model_name='program',
            name='priority',
            field=models.PositiveSmallIntegerField(default=10, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(10)]),
        ),
    ]
