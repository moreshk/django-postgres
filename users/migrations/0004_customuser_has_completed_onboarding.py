# Generated by Django 4.2.5 on 2023-10-20 08:40

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("users", "0003_customuser_user_type"),
    ]

    operations = [
        migrations.AddField(
            model_name="customuser",
            name="has_completed_onboarding",
            field=models.BooleanField(default=False),
        ),
    ]
