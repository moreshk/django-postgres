# Generated by Django 4.2.5 on 2023-10-29 03:41

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("users", "0014_graderesult_task_id"),
    ]

    operations = [
        migrations.AddField(
            model_name="graderesult",
            name="assignment_name",
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="graderesult",
            name="student_name",
            field=models.TextField(blank=True, null=True),
        ),
    ]
