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
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    active = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.pk} {self.title}'

class Bid(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    bid_price = models.DecimalField(decimal_places=2, max_digits=9)
    timestamp = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.user} bid {self.bid_price} on {self.listing}'

