# Generated by Django 4.2.5 on 2023-11-14 02:50

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("users", "0020_customuser_completed_lesson"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="customuser",
            name="completed_lesson",
        ),
    ]
