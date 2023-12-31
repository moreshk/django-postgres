# Generated by Django 4.2.5 on 2023-10-25 09:03

from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Rubric",
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
                ("name", models.CharField(max_length=255)),
                ("state", models.CharField(blank=True, max_length=255, null=True)),
                ("city", models.CharField(blank=True, max_length=255, null=True)),
                ("school", models.CharField(blank=True, max_length=255, null=True)),
                ("creater_id", models.PositiveIntegerField()),
                ("essay_type", models.CharField(max_length=255)),
                ("grade", models.CharField(blank=True, max_length=255, null=True)),
                ("curriculum", models.CharField(blank=True, max_length=255, null=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
            ],
            options={
                "verbose_name_plural": "rubrics",
                "db_table": "rubric",
            },
        ),
    ]
