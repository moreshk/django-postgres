# Generated by Django 4.2.5 on 2023-11-19 07:20

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("labeller", "0007_course_completion_token_bonus"),
        ("users", "0022_customuser_referral_slots"),
    ]

    operations = [
        migrations.AddField(
            model_name="customuser",
            name="completed_courses",
            field=models.ManyToManyField(
                related_name="completed_by_users", to="labeller.course"
            ),
        ),
    ]