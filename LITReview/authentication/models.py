from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    title = models.CharField(max_length=200, default="")
    pass