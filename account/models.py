from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.

class VideoflixUser(AbstractUser):
    email = models.EmailField(max_length=254, default='', unique=True)

    REQUIRED_FIELDS = ['email']