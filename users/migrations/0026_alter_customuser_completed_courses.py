# Generated by Django 4.2.5 on 2023-11-28 06:29

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("labeller", "0013_course_video_file_lesson_video_file"),
        ("users", "0025_customuser_language"),
    ]

    operations = [
        migrations.AlterField(
            model_name="customuser",
            name="completed_courses",
            field=models.ManyToManyField(
                blank=True, related_name="completed_by_users", to="labeller.course"
            ),
        ),
    ]
