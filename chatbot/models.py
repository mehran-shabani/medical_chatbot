from django.db import models
from django.core.validators import EmailValidator

class User(models.Model):
    name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=15, blank=True, null=True)  # Better to use CharField for phone numbers
    email = models.EmailField(max_length=254, validators=[EmailValidator()])  # Correct validator

    def __str__(self):
        return self.name

class ChatMessage(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    is_bot = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{'Bot' if self.is_bot else 'User'}: {self.message[:50]}"
class ChatSession(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)


class Disease(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    symptoms = models.ManyToManyField('Symptom', related_name='diseases')

class Symptom(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()


