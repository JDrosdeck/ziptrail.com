from django.db import models

class Waypoint(models.Model):
    waypoint = models.CharField(max_length=100)

    def __unicode__(self):
        return u'%s' % (self.waypoint)


class Route(models.Model):
    startAddress = models.CharField(max_length=200)
    endAddress = models.CharField(max_length=100)
    waypoints = models.ManyToManyField(Waypoint)
    totalMiles =  models.FloatField()
    gallonsGas = models.FloatField()
    leavingDate = models.DateTimeField(blank=True, null=True)

    def __unicode__(self):
        return u'%s - %s (Leaves on <%s>)' % (self.startAddress, self.endAddress, self.leavingDate)
