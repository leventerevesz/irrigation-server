# Generated by Django 2.2.2 on 2019-06-15 11:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('programs', '0007_program_priority'),
    ]

    operations = [
        migrations.RenameField(
            model_name='program',
            old_name='is_active',
            new_name='enabled',
        ),
    ]
