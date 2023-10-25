from django.db import models

# Create your models here.

class Rubric(models.Model):
    name = models.CharField(max_length=255, null=False)
    state = models.CharField(max_length=255, null=True, blank=True)
    city = models.CharField(max_length=255, null=True, blank=True)
    school = models.CharField(max_length=255, null=True, blank=True)
    creater_id = models.PositiveIntegerField(null=False)
    essay_type = models.CharField(max_length=255)
    grade = models.CharField(max_length=255, null=True, blank=True)
    curriculum = models.CharField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'rubric'
        verbose_name_plural = 'rubrics'


class Criteria(models.Model):
    rubric = models.ForeignKey(Rubric, on_delete=models.CASCADE)
    criteria_name = models.CharField(max_length=255)
    max_score = models.PositiveIntegerField()
    criteria_desc = models.TextField()
    spell_check = models.BooleanField(default=False)

    class Meta:
        db_table = 'criteria'
