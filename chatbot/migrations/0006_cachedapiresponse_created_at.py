# Generated by Django 4.2.5 on 2024-02-07 02:53

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):
    dependencies = [
        ("chatbot", "0005_cachedapiresponse_history_hash"),
    ]

    operations = [
        migrations.AddField(
            model_name="cachedapiresponse",
            name="created_at",
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
