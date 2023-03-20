from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    following = models.ManyToManyField("self", blank=True, related_name="followers", symmetrical=False)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)