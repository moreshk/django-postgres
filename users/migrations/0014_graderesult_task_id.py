# Generated by Django 4.2.5 on 2023-10-28 11:30

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("users", "0013_graderesult_rubric_id"),
    ]

    operations = [
        migrations.AddField(
            model_name="graderesult",
            name="task_id",
            field=models.IntegerField(blank=True, null=True),
        ),
    ]