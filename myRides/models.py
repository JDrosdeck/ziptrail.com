from django.db import models
from django.contrib.auth.models import User
from rideShare.vehicle.models import autoModel
from rideShare.routes.models import Route

class University(models.Model):
    name = models.CharField(max_length=30)

class Passenger(models.Model):
    user = models.ForeignKey(User)
    university = models.ForeignKey(University)

# This represents a model of a host of a ride. Basically a User,
# Vehicle, and university
class Host(models.Model):
    user = models.ForeignKey(User)
    university = models.ForeignKey(University)
    vehicle = models.ForeignKey(autoModel)

    def __unicode__(self):
        return u'%s' % (self.user.username)
    

#This represents a model of an individual ride. With a host and participants
class Ride(models.Model):
    rideHost = models.ForeignKey(Host)
    rideParticipants = models.ManyToManyField(Passenger)
    trip = models.ForeignKey(Route)
    
    def __unicode__(self):
        return u'%s, %s' % (self.rideHost.user.username, self.trip.startAddress)

