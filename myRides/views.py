from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.views.generic.simple import direct_to_template
from django.shortcuts import render_to_response
from django.contrib.sessions.models import Session
from django import forms

#Database models
from rideShare.myRides.models import Host, Ride, Passenger
from rideShare.routes.models import Waypoint, Route
from rideShare.vehicle.models import autoMaker, autoModel
from rideShare.common.forms import loginForm
from rideShare.myRides.forms import tripForm
from django.contrib.auth.models import User

import urllib2
import re
import simplejson
import datetime

# This is going to show a users home, and allow them to create a ride
# or join a ride
def home_View(request):
  
    #Make sure the user is logged in
    if request.user.is_authenticated():
                
        #get all the rides that their apart of as a passenger
        username = request.session['username']
        
        myRides = Ride.objects.filter(rideParticipants__id__exact=User.objects.filter(username=username)[0].id)
        
        #Check to see if they've added a new ride.
        if request.method =='POST':
            form = tripForm(request.POST)
            if form.is_valid():
                #The trip information
                startAddress = form.cleaned_data['startAddress']
                endAddress = form.cleaned_data['endAddress']
                leavingDate = form.cleaned_data['leavingDate']
                #Car information
                manufacturer = form.cleaned_data['manufacturer']
                carName = form.cleaned_data['name']
                freeSeats = form.cleaned_data['freeSeats']
                mpg = form.cleaned_data['mpg']
                

                # We can now grab the data from google maps
                baseUrl= "http://maps.google.com/maps/api/directions/json?origin="
                cleanedStartAddress = re.sub(' ', ',', startAddress)
                print cleanedStartAddress
                cleanedEndAddress = re.sub(' ', ',', endAddress)
                print cleanedEndAddress

                baseUrl = baseUrl + cleanedStartAddress + "&destination="
                baseUrl = baseUrl + cleanedEndAddress + "&sensor=false"
                
                print baseUrl

                mapData = urllib2.urlopen(baseUrl)
                mapData =  mapData.read()
                mapData = simplejson.loads(mapData)
                #Extract data from the directions
                if 'status' in mapData:
                    status = mapData['status']
                    print status
                    if status == "OK":

                        if 'routes' in mapData:
                            mapData = mapData['routes']
                            mapData =  dict(mapData[0])

                        if 'legs' in mapData:
                            mapData =  mapData['legs']
                            mapData = dict(mapData[0])
                
                            if 'distance' in mapData:
                                distance =  mapData['distance']
                                distance = distance['text']

                            if 'duration' in mapData:
                                duration = mapData['duration']
                                duration = duration['text']

                            #Save the full data to the db
                            rideHost = User.objects.filter(username=request.session['username'])
                            
                            
                            trip = Route(startAddress=startAddress, endAddress=endAddress, totalMiles=32, gallonsGas=32)

                            trip.save()
                            vehicle = autoModel.objects.filter(manufacturer=autoMaker.objects.filter(name=manufacturer), name=carName)
                            

                            passenger = Passenger.objects.filter(user=rideHost)
                            university = passenger[0].university
                            
                            
                            host = passenger[0]
                            newHost = Host(passenger=host, vehicle=vehicle[0])
                            newHost.save()
                            
                            newRide = Ride(rideHost=newHost, trip=trip)

                            newRide.save()
                            

                    else:
                        return HttpResponse("Start or End address not valid.")

        form = tripForm()
        return direct_to_template(request, 'home.html', { 'rides' : myRides, 'form' : form })

    else:
        form = loginForm()
        return direct_to_template(request, 'login.html', { 'form' : form })

