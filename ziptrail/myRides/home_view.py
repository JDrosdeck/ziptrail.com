from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic.simple import direct_to_template
from django.shortcuts import render_to_response
from django.contrib.sessions.models import Session
from django.conf import settings
from django.utils import simplejson as json
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned

#Database models
from myRides.models import Users, Trip, UsersTrip
from routes.models import Waypoint, Route, WaypointForm
from vehicle.models import Car
from geo.models import ZipCode, Position
from badges.views import getBadges

#Forms
from django import forms
from common.forms import loginForm
from myRides.forms import tripForm, waypointForm, joinTripForm

from search.views import getDistance
import datetime
import ziptrailUtils

def home_view(request):

    #Make sure the user is logged in
    if request.user.is_authenticated():
                
        #get all the rides that their apart of as a passenger
        user = User.objects.get(username=request.session['username'])
        rider = Users.objects.get(user=user)

        #Explination of whats going on here: In order to allow a person to remove themselves from a ride
        # we need to have the id of the ride they belong to as well as the id of the Users trip (Waypoint id)
 
        acceptedRideIDs =[]
        waypointName = []
        ridersTripId = []
        acceptedRides = Trip.objects.filter(acceptedPassengers__user__id__exact=rider.id, active=True)
        for x in acceptedRides:
            #This will append the id of the ride to the acceotedRideIDs list
            acceptedRideIDs.append(x.id)
           
            for y in x.acceptedPassengers.all():
                #This will append the riders tripId and the waypoint name for easy viewing in the template
                ridersTripId.append(y.id)
                waypointName.append(y.waypoint.title)
                     
        #This will combine the three lists above into one list. This needs to be done because in the django template
        # system there is no way to iterate over multiple lists in one pass like there is in regular python
        lst = [{'waypointName':t[0],'acceptedRides': t[1], 'id':t[2]} for t in zip(waypointName,acceptedRideIDs, ridersTripId)]
     

        #get all rides that their still pending on as a passenger
        pendingRides = Trip.objects.filter(pendingPassengers__user__id__exact=rider.id, 
                                           active=True)
        
        #This gets all available rides exlcluding the user from being an acceptedPassenger, pendingPassenger or host
        # Basically any ride they have nothing to do with
        allRides = Trip.objects.filter(host__university=rider.university, 
                                       active=True).exclude(acceptedPassengers__user__id__exact=rider.id).exclude(pendingPassengers__user__id__exact=rider.id).exclude(host=rider)

        #All the rides that the user is hosting
        HostedRides = Trip.objects.filter(host=rider, 
                                          active=True)
        
        #Check to see if they've added a new ride.
        #The ride information is all going to be created client side
        # with javascript. We will be recieving the following information about
        # the trip, Start Address, Start Zip, End Address, End Zip, Duration, 
        # Miles, and free seats

        if request.method =='POST':
            form = tripForm(request.POST)
            if form.is_valid():
                #The trip information
                startAddress = form.cleaned_data['startAddress']
                startZip = form.cleaned_data['startZip']
                endAddress = form.cleaned_data['endAddress']
                endZip = form.cleaned_data['endZip']
                leavingDate = form.cleaned_data['leavingDate']
                public = form.cleaned_data['public']
                customEndpoints = form.cleaned_data['customEndpoints']

                #Car information
                freeSeats = form.cleaned_data['freeSeats']
                
                host = User.objects.get(username=request.session['username'])
                host = Users.objects.get(user=host)
                host.car = Car.objects.get(seats=int(freeSeats))
                host.save()
                
                latStart, lngStart = ziptrailUtils.getGeocode(startAddress, startZip)
                latEnd, lngEnd = ziptrailUtils.getGeocode(endAddress, endZip)
                if latStart and lngStart and latEnd and lngEnd:
                    startLatLong, createdStart = Position.objects.get_or_create(latitude=latStart, 
                                                                                longitude=lngStart)
                    endLatLong, createdEnd = Position.objects.get_or_create(latitude=latEnd, 
                                                                            longitude=lngEnd)

                    #calculate the total miles
                    dist = getDistance(latStart,
                                       lngStart, 
                                       latEnd, 
                                       lngEnd)
                    
                    gas = dist/16
                    route = Route(startAddress=startAddress, 
                                  startZip=ZipCode.objects.get(zip=startZip), 
                                  startLat_Long=startLatLong, 
                                  endAddress=endAddress, 
                                  endZip=ZipCode.objects.get(zip=endZip), 
                                  endLat_Long=endLatLong, 
                                  totalMiles=dist, 
                                  gallonsGas=gas)
                    route.save()
                                                                   
                    #Create a new Trip, 
                    newRide = Trip(host=host, 
                                   trip=route, 
                                   public=public, 
                                   customEndpoints=customEndpoints)
                    newRide.save()
                    return HttpResponseRedirect(settings.BASE_URL + '/rides/home')
                else:
                    return HttpResponse('Couldn\'t geocode')

        user = User.objects.get(username=request.session['username'])
        user = Users.objects.get(user=user)
               
        badges = getBadges(request)

        form = tripForm()
        return direct_to_template(request, 
                                  'home.html', 
                                  { 'rides' : acceptedRides, 
                                    'form' : form, 
                                    'availableRides' : allRides, 
                                    'hostedRides' : HostedRides, 
                                    'userInfo': user, 
                                    'lst' : lst, 
                                    'badges' : badges 
                                    })
    
    else:
        form = loginForm()
        return direct_to_template(request, 
                                  'login.html', 
                                  { 'form' : form 
                                    })
