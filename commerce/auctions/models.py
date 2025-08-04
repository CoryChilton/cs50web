from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class Listing(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    bid_price_cents = models.PositiveIntegerField()
    image_url = models.URLField()
    category = models.CharField(max_length=63)

    def __str__(self):
        return self.title

