# Generated by Django 4.2.5 on 2023-11-14 02:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("labeller", "0002_lesson"),
        ("users", "0019_customuser_token"),
    ]

    operations = [
        migrations.AddField(
            model_name="customuser",
            name="completed_lesson",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="labeller.lesson",
            ),
        ),
    ]
