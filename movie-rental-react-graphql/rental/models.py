from __future__ import unicode_literals
from django.db import models

# Create your models here.
class MovieRental(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    movieId = models.IntegerField()
    rentalDate = models.DateTimeField(auto_now_add=True)