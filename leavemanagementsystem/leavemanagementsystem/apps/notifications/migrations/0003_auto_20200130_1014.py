# Generated by Django 2.2.1 on 2020-01-30 10:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notifications', '0002_notification_number_of_days'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notification',
            name='number_of_days',
            field=models.CharField(blank=True, default='0', max_length=256),
        ),
    ]
