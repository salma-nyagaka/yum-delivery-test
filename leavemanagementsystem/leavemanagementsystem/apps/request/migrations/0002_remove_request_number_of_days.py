# Generated by Django 2.2.1 on 2020-01-29 12:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('request', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='request',
            name='number_of_days',
        ),
    ]
