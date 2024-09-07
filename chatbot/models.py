from django.db import models
from django.contrib.auth import validators

class User(models.Model):
    name = models.CharField(max_length=255)
    phone_number = models.IntegerField(max_length=100, blank=True, null=True)
    EMAIL = models.EmailField(max_length=254, validators='emailvalidator',  )

class ChatMessage(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    is_bot = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{'Bot' if self.is_bot else 'User'}: {self.message[:50]}"

