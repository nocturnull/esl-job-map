# account/models.py
from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    name = models.CharField(blank=True, max_length=255)
    email = models.EmailField(blank=False, max_length=255, help_text='Required. Provide a valid email address.')

    def __str__(self):
        return self.email
