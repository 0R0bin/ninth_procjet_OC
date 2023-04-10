from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings

class User(AbstractUser):
    followed_members = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        through="UserFollows",
        related_name="followed",
    )


class UserFollows(models.Model):
    user = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="following",
    )
    followed_user = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="following_by",
    )

    class Meta:
        unique_together = ["user", "followed_user"]