# Generated by Django 2.2.5 on 2019-09-28 19:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('programs', '0019_auto_20190716_0622'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='program',
            name='time_end',
        ),
    ]
