# Generated by Django 2.2.2 on 2019-07-16 12:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('programs', '0019_auto_20190716_0622'),
    ]

    operations = [
        migrations.CreateModel(
            name='ScheduledRun',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start', models.DateTimeField()),
                ('duration', models.DurationField()),
                ('progress', models.FloatField()),
                ('program', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='programs.Program')),
            ],
        ),
        migrations.CreateModel(
            name='RequestedRun',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start', models.DateTimeField()),
                ('duration', models.DurationField()),
                ('program', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='programs.Program')),
            ],
        ),
    ]