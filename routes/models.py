from django.db import models
from rideShare.geo.models import ZipCode, Position


class Waypoint(models.Model):
    #The title is basically just so when a user enters in a play they'd like
    #to go we have some easy way for them to identify it
    #so we can keep a nice list of saved places that they can easily give out
    title = models.CharField(max_length=50, blank=True, null=True)
    waypoint = models.CharField(max_length=100)
    lat_long = models.ForeignKey(Position)

    def __unicode__(self):
        return u'%s, %s' % (self.waypoint, self.zipCode)

class Route(models.Model):
    startAddress = models.CharField(max_length=200)
    startZip = models.ForeignKey(ZipCode, related_name = "Start Zip")
    startLat_Long = models.ForeignKey(Position, related_name = "Start Pos")
    endAddress = models.CharField(max_length=100)
    endZip = models.ForeignKey(ZipCode, related_name = "End Zip")
    endLat_Long = models.ForeignKey(Position, related_name = "End Pos")
    waypoints = models.ManyToManyField(Waypoint)
    totalMiles =  models.FloatField()
    gallonsGas = models.FloatField()
    leavingDate = models.DateTimeField(blank=True, null=True)

    def __unicode__(self):
        return u'%s - %s (Leaves on <%s>)' % (self.startAddress, self.endAddress, self.leavingDate)
