#This model contains anything that relates to the persons car, make, model,
#miles, condition, seats...etc..etc  

from django.db import models


class autoMaker(models.Model):
    name = models.CharField(max_length=20)
    
    def __unicode__(self):
        return u'%s' % (self.name)

class autoModel(models.Model):
    manufacturer = models.ForeignKey(autoMaker)
    name = models.CharField(max_length = 10)
    seats = models.IntegerField(max_length = 8)
    mpg = models.IntegerField(max_length=3)

    def __unicode__(self):
        return u'%s' % (self.manufacturer)
