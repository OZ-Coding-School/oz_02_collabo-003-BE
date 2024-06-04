# Generated by Django 5.0.6 on 2024-06-04 03:04

import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("admins", "0002_remove_kluck_admin_adms_id"),
        ("gpt_prompts", "0001_initial"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="gptprompt",
            name="admins_id",
        ),
        migrations.AddField(
            model_name="gptprompt",
            name="user_id",
            field=models.ForeignKey(
                db_column="user_id",
                default=django.utils.timezone.now,
                on_delete=django.db.models.deletion.PROTECT,
                to="admins.kluck_admin",
            ),
            preserve_default=False,
        ),
    ]