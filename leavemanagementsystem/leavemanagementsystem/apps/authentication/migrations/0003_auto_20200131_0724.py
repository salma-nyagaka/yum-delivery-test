# Generated by Django 2.2.1 on 2020-01-31 07:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0002_auto_20200128_1202'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='user',
            options={'permissions': (('manage_users', 'Manage regular users.'), ('manage_staff', 'Manage the manager.'), ('impersonate_users', 'Impersonate users.'))},
        ),
    ]