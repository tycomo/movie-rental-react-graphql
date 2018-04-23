from __future__ import unicode_literals
from django.db import models

# Create your models here.
class MovieRental(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    movieId = models.IntegerField()
    title = models.TextField()
    posterPathURL = models.TextField()
    rentalDate = models.DateTimeField(auto_now_add=True)
    returnDate = models.DateTimeField(null=True)