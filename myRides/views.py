from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.views.generic.simple import direct_to_template
from django.shorcuts inport render_to_response
from django import forms

#Database models
from rideShare.myRides.models import Host, Ride
from rideShare.routes.models import Waypoint, Route
from rideShare.vehicle.models import autoMaker, autoModel

