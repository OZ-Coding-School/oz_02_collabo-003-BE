# Generated by Django 5.0.6 on 2024-06-14 02:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("kluck_notifications", "0001_initial"),
    ]

    operations = [
        migrations.RenameField(
            model_name="devicetoken",
            old_name="app_name",
            new_name="device_os",
        ),
        migrations.AlterUniqueTogether(
            name="devicetoken",
            unique_together={("token", "device_os")},
        ),
    ]
