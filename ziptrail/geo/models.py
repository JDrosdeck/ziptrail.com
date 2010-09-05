from django.db import models


class Position(models.Model):
    latitude = models.FloatField()
    longitude = models.FloatField()

    def __unicode__(self):
        return u'%s, %s' % (self.latitude, self.longitude)



class ZipCode(models.Model):
    zip = models.CharField(db_index=True, max_length=5)
    stateAbbrev = models.CharField(max_length=2)
    stateName = models.CharField(max_length=40)
    globalPos = models.ForeignKey(Position)
    
    def __unicode__(self):
        return u'%s' % (self.zip)
