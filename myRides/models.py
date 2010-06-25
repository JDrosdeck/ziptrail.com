from django.db import models
from django.contrib.auth.models import User
from rideShare.vehicle.models import autoModel


# This represents a model of a host of a ride. Basically a User,
# Vehicle, and start Stop address
class Host(models.Model):
    user = models.ForeignKey(User)
    vehicle = models.ForeignKey(autoModel)

    def __unicode__(self):
        return u'%s' % (self.user.username)
    

#This represents a model of an individual ride. With a host and participants
class Ride(models.Model):
    rideHost = models.ForeignKey(Host)
    rideParticipants = models.ManyToManyField(User)
    
    def __unicode__(self):
        return u'%s' % (self.rideHost.user.username)

