# Generated by Django 4.2.5 on 2023-10-23 23:45

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("users", "0007_assignment"),
    ]

    operations = [
        migrations.RenameField(
            model_name="assignment",
            old_name="desc",
            new_name="task_description",
        ),
    ]
