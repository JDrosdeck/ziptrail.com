from django.db import models
from django.contrib.auth.models import User


class RideMessages(models.Model):
    messageSender = models.ForeignKey(User, related_name='sender')
    messageReciever = models.ForeignKey(User, related_name='reciever')
    messageSubject = models.TextField(max_length=25)
    messageText = models.TextField(max_length=500)
    date = models.DateField(auto_now_add=True)

