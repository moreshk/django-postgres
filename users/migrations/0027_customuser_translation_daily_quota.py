# Generated by Django 4.2.5 on 2023-12-01 01:51

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("users", "0026_alter_customuser_completed_courses"),
    ]

    operations = [
        migrations.AddField(
            model_name="customuser",
            name="translation_daily_quota",
            field=models.IntegerField(default=10),
        ),
    ]
