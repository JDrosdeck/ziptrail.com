from django.db import models
from django.contrib.auth.models import User
from rideShare.vehicle.models import Car
from rideShare.routes.models import Route, Waypoint
from rideShare.geo.models import ZipCode, Position

class StudentEmail(models.Model):
    email = models.CharField(max_length=35)

    def __unicode__(self):
        return u'%s' % (self.email)

class University(models.Model):
    name = models.CharField(max_length=150)
    address = models.CharField(max_length=200)
    email = models.ManyToManyField(StudentEmail)
    zip = models.ForeignKey(ZipCode)
    latLng = models.ForeignKey(Position)
    
    def __unicode__(self):
        return u'%s' % (self.name)

class Users(models.Model):
    user = models.ForeignKey(User)
    university = models.ForeignKey(University)
    car = models.ForeignKey(Car, blank=True, null=True)
    waypoints = models.ManyToManyField(Waypoint, blank=True, null=True)
    def __unicode__(self):
        return u'%s' % (self.user.username)
# Note on how to use waypoints in USERS -> 
# When a user asks to be part of a new ride we add their wanted waypoint to their list of USERS waypoints
# We then take the ID of that waypoint and stick it in the list of waypoints for the TRIP. We can just filter on the waypoint ID
# in order to get the information back of what USERS it belongs to.


    

class Trip(models.Model):
    host = models.ForeignKey(Users)
    trip = models.ForeignKey(Route)
    acceptedPassengers = models.ManyToManyField(Users, blank=True, null=True, related_name='accepted passengers')
    pendingPassengers = models.ManyToManyField(Users, blank=True, null=True, related_name='pending passengers')
    public = models.BooleanField(blank=False, null=False, default=False)
    def __unicode__(self):
        return u'Host: %s, Start: %s, End: %s' % (self.host.user.username, self.trip.startAddress, self.trip.endAddress) 

