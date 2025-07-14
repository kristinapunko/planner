from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    pass


class Task(models.Model):
    PRIORITY_CHOICES = [
        ('high', 'Високий'),
        ('medium', 'Середній'),
        ('low', 'Низький'),
    ]
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    start_time = models.DateTimeField(null=True, blank=True) 
    end_time = models.DateTimeField(null=True, blank=True)
    no_deadline = models.BooleanField(default=False)
    description = models.TextField(blank=True)
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='medium')
    category = models.CharField(max_length=100, blank=True) 
    done = models.BooleanField(default=False)