#This model contains anything that relates to the persons car, make, model,
#miles, condition, seats...etc..etc  

from django.db import models

class Car(models.Model):
    seats = models.IntegerField(max_length = 8)

    def __unicode__(self):
        return u'%s' % (self.seats)
