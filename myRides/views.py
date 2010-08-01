from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.views.generic.simple import direct_to_template
from django.shortcuts import render_to_response
from django.contrib.sessions.models import Session
from django import forms
from django.conf import settings
from django.utils import simplejson as json

#Database models
from rideShare.myRides.models import Users, Trip
from rideShare.routes.models import Waypoint, Route
from rideShare.vehicle.models import Car
from rideShare.geo.models import ZipCode, Position

from rideShare.common.forms import loginForm
from rideShare.myRides.forms import tripForm
from django.contrib.auth.models import User

import datetime


# This is going to show a users home, and allow them to create a ride
# or join a ride

def home_View(request):

    #Make sure the user is logged in
    if request.user.is_authenticated():
                
        #get all the rides that their apart of as a passenger
        user = User.objects.get(username=request.session['username'])
        rider = Users.objects.filter(user=user)
        acceptedRides = Trip.objects.filter(acceptedPassengers__id__exact=rider)
        
        #get all rides that their still pending on as a passenger
        pendingRides = Trip.objects.filter(pendingPassengers__id__exact=rider)

        
        allRides = Trip.objects.filter().exclude(acceptedPassengers__id__exact=rider).exclude(pendingPassengers__id__exact=rider).exclude(host=rider)

        HostedRides = Trip.objects.filter(host=rider)


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
                #Car information
                freeSeats = form.cleaned_data['freeSeats']
                
                host = User.objects.get(username=request.session['username'])
                host = Users.objects.get(user=host)
                host.car=Car.objects.get(seats=int(freeSeats))
                host.save()
                            
                startLatLong = Position(latitude=0.0, longitude=0.0)
                endLatLong = Position(latitude=0.0, longitude=0.0)
                startLatLong.save()
                endLatLong.save()
                route = Route(startAddress=startAddress, startZip=ZipCode.objects.get(zip=startZip), startLat_Long=startLatLong, endAddress=endAddress, endZip=ZipCode.objects.get(zip=endZip), endLat_Long=endLatLong, totalMiles=32, gallonsGas=32)
                route.save()
                                                                     
                #Create a new Trip, 
                newRide = Trip(host=host, trip=route)
                newRide.save()
                return HttpResponseRedirect(settings.BASE_URL + '/rides/home')
            
        form = tripForm()
        user = User.objects.get(username=request.session['username'])
        user = Users.objects.get(user=user)
        return direct_to_template(request, 'home.html', { 'rides' : acceptedRides, 'form' : form, 'availableRides' : allRides, 'hostedRides' : HostedRides, 'user':user})
    
    else:
        form = loginForm()
        return direct_to_template(request, 'login.html', { 'form' : form })




def jsonifyResults(QuerySet):
    result = dict()
    tempResult = []
    for result in QuerySet:
        tempResult.append(result)
        result['results'] = tempResult
    return json.dumps(result)


#this function is for when a user wants to join a ride. They first need to ask permission from the host
# if they are allowed to join
def askToJoinRide(request):

    if request.method == 'GET':
        if request.user.is_authenticated:
            tripId = request.GET.get('tripId', '')
            
            user = request.session['username']

            #check for proper input
            if tripId and user:
                
                try:
                    #Try and get the trip based on the tripId given
                    trip = Trip.objects.get(id=tripId)
                    #Try and get the rider based on the user
                    user = User.objects.get(username=user)
                    rider = Users.objects.get(user=user)
                    #Try and add the rider to the trip
                    trip.pendingPassengers.add(rider)
                    trip.save()
                except:
                    return HttpResponse('Not added')

                #Return the list of the users pending trips
                #return HttpResponse(jsonifyResults(Trip.objects.filter(pendingPassengers__id__exact=Users.objects.filter(user=user))))
                return HttpResponse('added')
            return HttpResponse('wrong input')
        return HttpResponse('not authenticated')
    return HttpResonse('wrong request type')


#this function is for when the host of ride wants to move a user from being a pending rider to being a member of the ride.
def addPendingRiderToRide(request):
    if request.method == 'GET':
        if request.user.is_authenticated:
            #we need the id of the Trip to add the user to
            tripId = request.GET.get('tripId', '')
            #We need the id of the rider to add to the trip.
            #The riderId given should be the id of the USER
            riderId = request.GET.get('riderId','')
            
            if tripId and riderId:
               try:
                   #Get the trip
                   trip = Trip.objects.get(id=tripId)
                   rider = Users.objects.get(user=riderId)
                
                   trip.acceptedPassengers.add(rider)
                   trip.pendingPassengers.remove(rider)
                   trip.save()
                   return HttpResponse('Rider added to trip, pending rider removed')
               except:
                   return HttpResponse('')
            return HttpResponse('import args')
        return HttpResponse('not authenticated')
    return HttpResponse('wrong request type')
            

def removeRiderFromRide(request):
    if request.method == 'GET':
        if user.is_authenticated:
                #we need the id of the Trip to add the user to                                                                                          
            tripId = request.GET.get('tripId', '')

                #We need the id of the rider to remove from the trip.                                                                                 
                #The riderId given should be the id of the USER                                                                                        
            riderId = request.GET.get('riderId','')

            if tripId and riderId:
                try:
                   #Get the trip                                                                                                                   
                    trip = Trip.objects.get(id=tripId)
                    rider = Users.objects.get(user=riderId)

                    trip.acceptedPassengers.remove(rider)
                    trip.save()
                    return HttpResponse('Rider removed from trip')
                except:
                    return HttpResponse('')
            return HttpResponse('import args')
        return HttpResponse('not authenticated')
    return HttpResponse('wrong request type')


def viewRide(request, id):
    # id represents the ID of the TRIP
    # We want to show detailed information about the trip
    # ie. google map. Waypoints, people involved
    
    matchedTrip = Trip.objects.get(id=id)
    
    return direct_to_template(request, 'view.html', { 'trip' : matchedTrip })
