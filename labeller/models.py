from django.db import models
from django.db.models import JSONField
from django.conf import settings


class Course(models.Model):
    name = models.CharField(max_length=200, null=False, blank=False)
    description = models.TextField(null=False, blank=False)
    logo = models.ImageField(upload_to='logos/', null=True, blank=True)
    completion_token_bonus = models.IntegerField(default=0)
    video_link = models.TextField(null=True, blank=True)
    transcript = models.TextField(null=True, blank=True)
    timed_transcripts = models.TextField(null=True, blank=True)
    creator = models.ForeignKey('users.CustomUser', on_delete=models.CASCADE, related_name='created_courses', null=True)
    video_file = models.FileField(upload_to='videos/', null=True, blank=True)

    def __str__(self):
        return self.name
    


class Lesson(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    step_id = models.IntegerField()
    dialog = models.TextField()
    image_path = models.ImageField(upload_to='images/', null=True, blank=True)
    audio_path = models.FileField(upload_to='audio/', null=True, blank=True)
    user_options = JSONField(null=True, blank=True)
    correct_answer = models.IntegerField(null=True, blank=True)
    youtube_video_url = models.URLField(null=True, blank=True)
    correct_answer_image = models.ImageField(upload_to='images/', null=True, blank=True)
    headline = models.CharField(max_length=200, null=True, blank=True)  # new field
    start_time = models.TimeField(null=True, blank=True)
    end_time = models.TimeField(null=True, blank=True)
    video_file = models.FileField(upload_to='videos/', null=True, blank=True)
    def __str__(self):
        return f"{self.course.name} - Step {self.step_id}"
    

class UserLessonProgress(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    course = models.ForeignKey('labeller.Course', on_delete=models.CASCADE)
    lesson = models.ForeignKey('labeller.Lesson', on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'course')