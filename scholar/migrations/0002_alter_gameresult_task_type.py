# Generated by Django 4.2.5 on 2024-01-02 03:23

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("scholar", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="gameresult",
            name="task_type",
            field=models.CharField(
                choices=[
                    ("addition", "Addition"),
                    ("multiplication", "Multiplication"),
                    ("subtraction", "Subtraction"),
                ],
                max_length=20,
            ),
        ),
    ]
