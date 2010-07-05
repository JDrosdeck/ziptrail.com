from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.views.generic.simple import direct_to_template
from django.shortcuts import render_to_response
from django.contrib.sessions.models import Session
from django import forms

#Database models
from rideShare.myRides.models import Users, TripPassengers, Trip
from rideShare.routes.models import Waypoint, Route
from rideShare.vehicle.models import Car
from rideShare.zip.models import ZipCode

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
        

        user = User.objects.get(username=username)
        myRides = Trip.objects.filter(passengers__id__exact=Users.objects.filter(user=user))
        print len(myRides)
        
        allRides = Trip.objects.filter().exclude(passengers__id__exact=Users.objects.filter(user=user))
        print len(allRides)

        #Check to see if they've added a new ride.
        if request.method =='POST':
            form = tripForm(request.POST)
            if form.is_valid():
                #The trip information
                startAddress = form.cleaned_data['startAddress']
                startZip = form.cleaned_data['startZip']
                endAddress = form.cleaned_data['endAddress']
                endZip = form.cleaned_data['endZip']
                leavingDate = form.cleaned_data['leavingDate']
                #Car information
                freeSeats = form.cleaned_data['freeSeats']
                
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
                            host = User.objects.get(username=request.session['username'])
                            host = Users.objects.get(user=host)
                            host.car=Car.objects.get(seats=freeSeats)
                            host.save()
                            

                            route = Route(startAddress=startAddress, startZip=ZipCode.objects.get(zip=startZip), endAddress=endAddress, endZip=ZipCode.objects.get(zip=endZip), totalMiles=32, gallonsGas=32)
                            route.save()
                                                                     
                            #Create a new Trip, 
                            newRide = Trip(host=host, trip=route)
                            newRide.save()
                            return HttpResponseRedirect('/rides/home')

                    else:
                        return HttpResponse("Start or End address not valid.")

        form = tripForm()
        return direct_to_template(request, 'home.html', { 'rides' : myRides, 'form' : form, 'availableRides' : allRides })

    else:
        form = loginForm()
        return direct_to_template(request, 'login.html', { 'form' : form })

def removePassengerFromRide(request, id):
    # id presents the ID of the TRIP
    # we need to remove the requested user from being a passenger in the trip
    if request.user.is_authenticated():
        username = request.session['username']

        user = User.objects.filter(username=username)
        currentUser = Users.objects.get(user=user)
        passenger = TripPassengers.objects.get(id=currentUser.id)
        print passenger

        if passenger:
        #Select from Trip where TripPassenger = username and id = given id
            trip = Trip.objects.filter(id=id, passengers__id__exact=Users.objects.get(user=user).id)
            print len(trip)
            if len(trip) > 0:
                trip[0].passengers.remove(passenger)
                trip[0].save()
                print trip[0].passengers.all()
                
                return HttpResponseRedirect('/rides/home/')
        
        return HttpResponse("You don't seem to be apart of this ride anyway")
   
def addPassengerToRide(request, id):
    # id represents the ID of the TRIP
    # We need to add the requested user to be a passenger in the trip
    if request.user.is_authenticated():
        username = request.session['username']

        user = User.objects.filter(username=username)
        currentUser = Users.objects.get(user=user)
        passenger = TripPassengers.objects.get(id=currentUser.id)

        trip = Trip.objects.filter(id=id)
        if len(trip) > 0:
            trip[0].passengers.add(passenger)
            trip[0].save()
            
            return HttpResponseRedirect('/rides/home/')
        
        else:
            return HttpResponse("You're already apart of this ride")

    else:
        return HttpResponseRedirect('/login/')

def viewRide(request, id):
    # id represents the ID of the TRIP
    # We want to show detailed information about the trip
    # ie. google map. Waypoints, people involved
    
    matchedTrip = Trip.objects.get(id=id)
    print matchedTrip.passengers


    return direct_to_template(request, 'view.html', { 'trip' : matchedTrip })
