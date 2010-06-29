from django.db import models
from django.contrib.auth.models import User
from rideShare.vehicle.models import Car
from rideShare.routes.models import Route

class University(models.Model):
    name = models.CharField(max_length=30)
    
    def __unicode__(self):
        return u'%s' % (self.name)

class Users(models.Model):
    user = models.ForeignKey(User)
    university = models.ForeignKey(University)
    car = models.ForeignKey(Car)

    def __unicode__(self):
        return u'%s' % (self.user.username)
    
class TripPassengers(models.Model):
    passenger = models.ForeignKey(Users)

    def __unicode__(self):
        return u'%s' % (self.passenger.Users.user.username)

class Trip(models.Model):
    host = models.ForeignKey(Users)
    trip = models.ForeignKey(Route)
    passengers = models.ForeignKey(TripPassengers)

    def __unicode__(self):
        return u'Host: %s, Start: %s, End: %s' % (self.host.Users.user.username, self.trip.startAddress, self.trip.endAddress) 

