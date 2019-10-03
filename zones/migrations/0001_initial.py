# Generated by Django 2.2.5 on 2019-10-03 15:01

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('controllers', '0004_auto_20190711_0542'),
    ]

    operations = [
        migrations.CreateModel(
            name='Zone',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=80)),
                ('location', models.CharField(blank=True, default='', max_length=80)),
                ('description', models.TextField(blank=True, default='')),
                ('enabled', models.BooleanField(default=True)),
                ('channels', models.ManyToManyField(blank=True, to='controllers.Channel')),
            ],
        ),
    ]
