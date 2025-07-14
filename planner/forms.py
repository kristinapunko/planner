from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser
from django import forms
from .models import Task

class RegisterUserForm(UserCreationForm):
    class Meta:
        model = CustomUser  
        fields = ("username", "email", "password1", "password2")

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'start_time', 'end_time', 'priority', 'category', 'done']