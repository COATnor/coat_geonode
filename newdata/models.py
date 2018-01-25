from django.db import models

# Create your models here.


class Moth(models.Model):
    date = models.DateTimeField()
    alt = models.IntegerField()
    location = models.CharField(max_length=12)
    waypoint = models.CharField(max_length=12)
    station = models.PositiveSmallIntegerField()
    ep = models.PositiveIntegerField()
    opl = models.PositiveIntegerField()
    opint = models.PositiveIntegerField()
    opdark = models.PositiveIntegerField()
    opsum = models.PositiveIntegerField()
    agr = models.PositiveIntegerField()
    obs = models.CharField(max_length=12)
    branches = models.PositiveSmallIntegerField()
    notes = models.CharField()

