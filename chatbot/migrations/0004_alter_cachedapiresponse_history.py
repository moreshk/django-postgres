# Generated by Django 4.2.5 on 2024-02-05 23:53

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("chatbot", "0003_cachedapiresponse_audio_response"),
    ]

    operations = [
        migrations.AlterField(
            model_name="cachedapiresponse",
            name="history",
            field=models.JSONField(blank=True, null=True),
        ),
    ]
