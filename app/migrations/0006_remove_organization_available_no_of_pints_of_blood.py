# Generated by Django 5.1.4 on 2024-12-12 06:16

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("app", "0005_user_user_type"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="organization",
            name="available_no_of_pints_of_blood",
        ),
    ]