# Generated by Django 4.2.5 on 2023-11-01 03:52

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("v3essay_grader", "0004_combinedpromptresults_created_at"),
    ]

    operations = [
        migrations.DeleteModel(
            name="CombinedPromptResults",
        ),
    ]