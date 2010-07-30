from django.db import models

class badges(models.Model):
    name = models.CharField(max_length=15)
    
    def __unicode__(self):
        return u'%s' % (self.name)
