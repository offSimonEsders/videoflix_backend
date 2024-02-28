from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.crypto import get_random_string


# Create your models here.

class VideoflixUser(AbstractUser):
    email = models.EmailField(max_length=254, default='', unique=True)
    verified = models.BooleanField(default=False)
    verification_code = models.CharField(max_length=30, default=get_random_string(length=30), blank=True, unique=True)
    reset_code = models.CharField(max_length=100, blank=True, null=True, unique=False)
    REQUIRED_FIELDS = ['email']

    def create_reset_code(self):
        self.reset_code = get_random_string(length=30) + self.email
        self.save()
