from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    follow = models.ManyToManyField("self", blank=True, related_name="followers", symmetrical=False)
    # follow = models.ManyToManyField("self", through='UserFollows')
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

class UserFollows(models.Model):
    follows = models.ForeignKey(to=CustomUser, related_name='user', on_delete=models.CASCADE)
    followed_user = models.ForeignKey(to=CustomUser, on_delete=models.CASCADE)

    class Meta:
        unique_together=('follows', 'followed_user')