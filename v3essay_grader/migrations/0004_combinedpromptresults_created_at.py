# Generated by Django 4.2.5 on 2023-11-01 03:44

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):
    dependencies = [
        ("v3essay_grader", "0003_combinedpromptresults"),
    ]

    operations = [
        migrations.AddField(
            model_name="combinedpromptresults",
            name="created_at",
            field=models.DateTimeField(
                auto_now_add=True, default=django.utils.timezone.now
            ),
            preserve_default=False,
        ),
    ]
