# Generated by Django 4.2.5 on 2023-11-11 04:57

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("users", "0017_customuser_referral_code_customuser_referred_by"),
    ]

    operations = [
        migrations.AddField(
            model_name="customuser",
            name="wallet",
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name="customuser",
            name="user_type",
            field=models.CharField(
                choices=[
                    ("TEACHER", "Teacher"),
                    ("STUDENT", "Student"),
                    ("PARENT", "Parent"),
                    ("ADMINISTRATOR", "Administrator"),
                    ("LABELLER", "Labeller"),
                ],
                default="Student",
                max_length=15,
            ),
        ),
    ]