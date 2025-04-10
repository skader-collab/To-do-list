from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model

# Create your models here.
# User model
class User(AbstractUser):
    username = models.CharField(max_length=100, unique=True)
    password = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.username

    
class Task(models.Model):
    userid = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tasks')
    title = models.CharField(max_length=100)
    description = models.TextField()
    due_date = models.DateTimeField()
    is_completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.title