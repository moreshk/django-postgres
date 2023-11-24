# Generated by Django 4.2.5 on 2023-11-24 02:04

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("labeller", "0012_lesson_end_time_lesson_start_time"),
    ]

    operations = [
        migrations.AddField(
            model_name="course",
            name="video_file",
            field=models.FileField(blank=True, null=True, upload_to="videos/"),
        ),
        migrations.AddField(
            model_name="lesson",
            name="video_file",
            field=models.FileField(blank=True, null=True, upload_to="videos/"),
        ),
    ]
