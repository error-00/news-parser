from django.db import models
from django.contrib.auth.models import AbstractUser
from parser_app.models import Articles


class User(AbstractUser):
    image = models.ImageField(upload_to="users_images", blank=True, null=True)
    saved_articles = models.ManyToManyField(Articles, related_name="saved_by", blank=True)

    def __str__(self) -> str:
        return self.username
