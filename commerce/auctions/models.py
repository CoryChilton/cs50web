from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    # watchlist listings
    listings = models.ManyToManyField('Listing', blank=True, related_name='users_watching')
    

class Listing(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    bid_price = models.DecimalField(decimal_places=2, max_digits=9)
    image_url = models.URLField()
    category = models.CharField(max_length=63)

    def __str__(self):
        return f'{self.pk} {self.title}'

