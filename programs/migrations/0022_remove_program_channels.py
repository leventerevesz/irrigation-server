# Generated by Django 2.2.5 on 2019-10-03 15:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('programs', '0021_program_can_be_skipped'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='program',
            name='channels',
        ),
    ]
