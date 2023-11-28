# Generated by Django 4.2.5 on 2023-11-19 22:55

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("users", "0023_customuser_completed_courses"),
    ]

    operations = [
        migrations.CreateModel(
            name="GlobalSettings",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("referring_user_bonus", models.IntegerField(default=100)),
                ("referred_user_bonus", models.IntegerField(default=100)),
            ],
        ),
    ]