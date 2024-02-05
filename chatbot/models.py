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
    

# chatbot/models.py

class CachedResponse(models.Model):
    user_input = models.TextField()
    conversation_history = models.JSONField()  # Stores the list of previous interactions
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)  # Link to the Topic model
    api_response = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [
            models.Index(fields=['user_input', 'topic']),  # Index to speed up searches
        ]

    def __str__(self):
        return f"CachedResponse for {self.topic}"