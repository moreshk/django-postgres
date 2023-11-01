# Generated by Django 4.2.5 on 2023-11-01 03:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("v3essay_grader", "0005_delete_combinedpromptresults"),
    ]

    operations = [
        migrations.CreateModel(
            name="CombinedPromptResults",
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
                ("user_response", models.TextField()),
                ("ai_feedback", models.TextField()),
                ("title", models.CharField(max_length=255)),
                ("description", models.TextField()),
                ("essay_type", models.CharField(max_length=255)),
                ("grade", models.CharField(max_length=255)),
                ("rubric_name", models.CharField(max_length=255)),
                (
                    "assignment_name",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
                (
                    "student_name",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
                ("user_id", models.PositiveIntegerField()),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                (
                    "rubric",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="v3essay_grader.rubric",
                    ),
                ),
            ],
            options={
                "db_table": "combined_prompt_results",
            },
        ),
    ]