from django.db import models
from django.contrib.auth.models import User
from rideShare.vehicle.models import Car
from rideShare.routes.models import Route, Waypoint
from rideShare.geo.models import ZipCode, Position
from django.forms import ModelForm


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

class UsersTrip(models.Model):
    user = models.ForeignKey(Users)
    waypoint = models.ForeignKey(Waypoint, blank=True, null=True)

    def __unicode__(self):
        return u'%s, %s' % (self.user.user.username, self.waypoint.waypoint)

    #waypoints in USERS is used so that we can save their custom waypoints so that they can
    # easily add them again to another ride without having to reenter them. And we don't have to
    # re-grab the information from a mapping service

    #pendingWaypoints is used in TRIP to make it easier to map the USERS to the waypoints. When they are accepted
    # to the trip we add it to the trips actual waypoint list.

class Trip(models.Model):
    host = models.ForeignKey(Users)
    trip = models.ForeignKey(Route)
    acceptedPassengers = models.ManyToManyField(UsersTrip, blank=True, null=True, related_name='accepted passengers')
    pendingPassengers = models.ManyToManyField(UsersTrip, blank=True, null=True, related_name='pending passengers')
    public = models.BooleanField(blank=False, null=False, default=False)
    MaskEndpoint = models.BooleanField(blank=False, null=False, default=False)
    def __unicode__(self):
        return u'Host: %s, Start: %s, End: %s' % (self.host.user.username, self.trip.startAddress, self.trip.endAddress) 

