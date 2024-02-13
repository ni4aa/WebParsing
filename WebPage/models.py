from django.db import models
import datetime
from celery.schedules import crontab
from django.dispatch import receiver


class CarModel(models.Model):
    name = models.CharField(max_length=256)
    description = models.TextField(null=True)
    image = models.URLField(null=True)
    price = models.DecimalField(max_digits=8, decimal_places=2, null=True)
    auction = models.CharField(max_length=256)
    lot_number = models.TextField()
    miles = models.TextField(null=True)
    url = models.URLField(null=True)
    date = models.DateTimeField(null=True)

