# Generated by Django 4.2.5 on 2023-11-12 00:38

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("users", "0018_customuser_wallet_alter_customuser_user_type"),
    ]

    operations = [
        migrations.AddField(
            model_name="customuser",
            name="token",
            field=models.IntegerField(default=0),
        ),
    ]
