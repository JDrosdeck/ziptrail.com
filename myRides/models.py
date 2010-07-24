from django.db import models
from django.contrib.auth.models import User
from rideShare.vehicle.models import Car
from rideShare.routes.models import Route
from rideShare.zip.models import ZipCode, Position

class StudentEmail(models.Model):
    email = models.CharField(max_length=10)

    def __unicode__(self):
        return u'%s' % (self.email)

class University(models.Model):
    name = models.CharField(max_length=30)
    address = models.CharField(max_length=50)
    email = models.ManyToManyField(StudentEmail)
    zip = models.ForeignKey(ZipCode)
    latLng = models.ForeignKey(Position)
    
    def __unicode__(self):
        return u'%s' % (self.name)

class Users(models.Model):
    user = models.ForeignKey(User)
    university = models.ForeignKey(University)
    car = models.ForeignKey(Car, blank=True, null=True)

    def __unicode__(self):
        return u'%s' % (self.user.username)
    
class TripPassengers(models.Model):
    passenger = models.ForeignKey(Users)

    def __unicode__(self):
        return u'%s' % (self.passenger.user.username)

class Trip(models.Model):
    host = models.ForeignKey(Users)
    trip = models.ForeignKey(Route)
    passengers = models.ManyToManyField(TripPassengers, blank=True, null=True)
    public = models.BooleanField(blank=False, null=False, default=False)
    def __unicode__(self):
        return u'Host: %s, Start: %s, End: %s' % (self.host.user.username, self.trip.startAddress, self.trip.endAddress) 

