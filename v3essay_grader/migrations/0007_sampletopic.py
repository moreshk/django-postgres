# Generated by Django 4.2.5 on 2023-11-06 07:51

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("v3essay_grader", "0006_combinedpromptresults"),
    ]

    operations = [
        migrations.CreateModel(
            name="SampleTopic",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("essay_type", models.CharField(max_length=255)),
                ("essay_title", models.CharField(max_length=255)),
                ("essay_description", models.TextField()),
                ("creator_id", models.PositiveIntegerField()),
                ("grade", models.IntegerField(blank=True, null=True)),
            ],
            options={
                "db_table": "sample_topics",
            },
        ),
    ]
