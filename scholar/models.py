from django.db import models
from django.utils import timezone
from users.models import CustomUser

class GameResult(models.Model):
    TASK_TYPES = (
        ('addition', 'Addition'),
        ('multiplication', 'Multiplication'),
        ('subtraction', 'Subtraction'),
        # Add more task types if needed
    )

    timestamp = models.DateTimeField(default=timezone.now)
    task_type = models.CharField(max_length=20, choices=TASK_TYPES)
    correct_answers_count = models.IntegerField()
    wrong_answers_count = models.IntegerField()
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.email} - {self.task_type} - {self.timestamp.strftime('%Y-%m-%d %H:%M:%S')}"
    

    # scholar/models.py

class ScreenTime(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    operation = models.CharField(max_length=20)
    timestamp = models.DateTimeField(default=timezone.now)
    minutes = models.IntegerField()

    def __str__(self):
        return f"{self.user.email} - {self.operation} - {self.minutes} minutes - {self.timestamp.strftime('%Y-%m-%d %H:%M:%S')}"