# Generated by Django 2.2.2 on 2019-07-09 05:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('controllers', '0002_channel_location'),
    ]

    operations = [
        migrations.AddField(
            model_name='controller',
            name='location',
            field=models.CharField(blank=True, default='', max_length=80),
        ),
    ]
