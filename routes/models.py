from django.db import models

class Route(models.Model):
    MeetingPlace = models.TextField(max_length=200)
    totalMiles =  models.FloatField()
    gallonsGas = models.FloatField()
