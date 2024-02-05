from django.db import models


class Topic(models.Model):
    topic = models.CharField(max_length=200, null=False, blank=False)
    description = models.TextField(null=False, blank=False)
    genre = models.CharField(max_length=100, null=False, blank=False)
    subgenre = models.TextField(null=False, blank=False)
    step_id = models.IntegerField(null=False, blank=False)
    image = models.ImageField(upload_to='topics/', null=True, blank=True)

    def __str__(self):
        return self.topic
    
class CachedAPIResponse(models.Model):
    topic = models.CharField(max_length=200)
    history = models.JSONField()  # Updated to use the new JSONField
    message = models.TextField()
    response = models.TextField()
    audio_response = models.FileField(upload_to='audio_responses/', null=True, blank=True)

    class Meta:
        indexes = [
            models.Index(fields=['topic', 'message']),
        ]

    def __str__(self):
        return f"Cached response for topic {self.topic}"