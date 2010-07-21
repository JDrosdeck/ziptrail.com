from django.db import models

class ZipCode(models.Model):
    zip = models.CharField(db_index=True, max_length=5)
    stateAbbrev = models.CharField(max_length=2)
    stateName = models.CharField(max_length=15)
    longitude = models.FloatField()
    latitude = models.FloatField()
    
    def __unicode__(self):
        return u'%s' % (self.zip)
