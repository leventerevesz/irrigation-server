# Generated by Django 2.2.2 on 2019-07-11 05:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('controllers', '0003_controller_location'),
    ]

    operations = [
        migrations.AlterField(
            model_name='channel',
            name='channel_no',
            field=models.PositiveSmallIntegerField(),
        ),
        migrations.AlterField(
            model_name='controller',
            name='channel_count',
            field=models.PositiveSmallIntegerField(),
        ),
    ]
