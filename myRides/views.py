from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.views.generic.simple import direct_to_template
from django.shortcuts import render_to_response
from django.contrib.sessions.models import Session
from django import forms
from django.conf import settings
from django.utils import simplejson as json

#Database models
from rideShare.myRides.models import Users, TripPassengers, Trip
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
        myRides = Trip.objects.filter(passengers__id__exact=Users.objects.filter(user=user))

        
        allRides = Trip.objects.filter().exclude(passengers__id__exact=Users.objects.filter(user=user)).exclude(host=Users.objects.get(user=user))

        HostedRides = Trip.objects.filter(host=Users.objects.get(user=user))

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
            
        #This is for adding a ride via ajax
        elif request.method == 'GET':
            startAdd = request.GET.get('startAdd' , '')
            startZip = request.GET.get('startZip', '')
            startLat = request.GET.get('startLat', '')
            startLng = request.GET.get('startLng', '')
            endAdd = request.GET.get('endAdd', '')
            endZip = request.GET.get('endZip', '')
            endLat = request.GET.get('endLat', '')
            endLng = request.GET.get('endLng', '')
            seats = request.GET.get('seats', '')
            if startAdd != '' and startZip != '' and startLat != '' and startLng != '' and endAdd != '' and endZip != '' and endLat != '' and endLng != '' and seats!= '':
                host = User.objects.get(username=request.session['username'])
                host = Users.objects.get(user=host)
                host.car=Car.objects.get(seats=int(seats))
                host.save()
                
                startLatLong = Position(latitude=startLat, longitude=startLng)
                endLatLong = Position(latitude=endLat, longitude=endLng)
                startLatLong.save()
                endLatLong.save()
                route = Route(startAddress=startAdd, startZip=ZipCode.objects.get(zip=startZip), startLat_Long=startLatLong, endAddress=endAdd, endZip=ZipCode.objects.get(zip=endZip), endLat_Long=endLatLong, totalMiles=32, gallonsGas=32)
                route.save()
                newRide = Trip(host=host, trip=route)
                newRide.save()	
	        g = Trip.objects.filter(host=Users.objects.filter(user=user))

                return HttpResponse(g)


        form = tripForm()
        return direct_to_template(request, 'home.html', { 'rides' : myRides, 'form' : form, 'availableRides' : allRides, 'hostedRides' : HostedRides })
    

    else:
        form = loginForm()
        return direct_to_template(request, 'login.html', { 'form' : form })

def removePassengerFromRideAjax(request):
    if request.method == 'GET':
        if request.user.is_authenticated():
            try:
                username = request.session['username']
            except:
                #We couldn't get the login name
                #redirect to the login
                return HttpResponseRedirect(settings.BASE_URL + '/login/')
            user = User.objects.filter(username=username)
            currentUser = Users.objects.get(user=user)
            passenger = TripPassengers.objects.get(id=currrentUser.id)
        
            
            #Select from trip where trippassenger = username and id = given id
            trip = Trip.objects.filter(id=id, passenger__id__exact=Users.objects.get(user=user).id)
            if len(trip) > 0:
                trip[0].passengers.remove(passenger)
                trip[0].save()
                results = jsonifyResults(Trip.objects.filter(passengers__id__exact=Users.objects.filter(user=user)))                                      
                return HttpResponse(results)
        else:
            return HttpResponseRedirect(settings.BASE_URL + '/login/')


#This function will probably be taken out. The ajax version will be used instead
def removePassengerFromRide(request, id):
    # id presents the ID of the TRIP
    # we need to remove the requested user from being a passenger in the trip
    if request.user.is_authenticated():
        
        try:
            username = request.session['username']
        except:
            #We couldn't get the login name
            #redirect to the login
            return HttpResponseRedirect(settings.BASE_URL + '/login/')

        user = User.objects.filter(username=username)
        currentUser = Users.objects.get(user=user)
        passenger = TripPassengers.objects.get(id=currentUser.id)
       
        if passenger:
            #Select from Trip where TripPassenger = username and id = given id
            trip = Trip.objects.filter(id=id, passengers__id__exact=Users.objects.get(user=user).id)

            if len(trip) > 0:
                trip[0].passengers.remove(passenger)
                trip[0].save()
                
                return HttpResponseRedirect(settings.BASE_URL + '/rides/home/')
        
        return HttpResponse("You don't seem to be apart of this ride anyway")


def addPassengerToRideAJAX(request):
    if request.method == 'GET':
        id = request.GET.get('id', '')
        if request.user.is_authenticated():
            user = User.objects.filter(username=username)
            currentUser = Users.objects.get(user=user)
            try:
                passenger = TripPassengers.objects.get(id=currentUser.id)
            except:
                passenger = TripPassengers(passenger=currentUser)
                passenger.save()
                passenger = TripPassengers.objects.get(id=currentUser.id)

            trip = Trip.objects.get(id=id)
            trip.passenger.add(passenger)
            trip.save()
            results = jsonifyResults(Trip.objects.filter(passengers__id__exact=Users.objects.filter(user=user)))
            return HttpResponse(results)
        else:
            return HttpResponseRedirect(settings.BASE_URL + '/login/')


def jsonifyResults(QuerySet):
    result = dict()
    tempResult = []
    for result in QuerySet:
        tempResult.append(result)
        result['results'] = tempResult
    return json.dumps(result)

#This will probably be removed instead we will use the ajax versions
def addPassengerToRide(request, id):
    # id represents the ID of the TRIP
    # We need to add the requested user to be a passenger in the trip
    if request.user.is_authenticated():
        username = request.session['username']

        user = User.objects.filter(username=username)
        currentUser = Users.objects.get(user=user)
        try:
            passenger = TripPassengers.objects.get(id=currentUser.id)
        except:
            passenger = TripPassengers(passenger=currentUser)
            passenger.save()
            passenger = TripPassengers.objects.get(id=currentUser.id)
        

        trip = Trip.objects.get(id=id)
        
        trip.passengers.add(passenger)
        trip.save()
            
        return HttpResponseRedirect(settings.BASE_URL + '/rides/home/')
        
    else:
        return HttpResponseRedirect('/login/')

def viewRide(request, id):
    # id represents the ID of the TRIP
    # We want to show detailed information about the trip
    # ie. google map. Waypoints, people involved
    
    matchedTrip = Trip.objects.get(id=id)
    
    return direct_to_template(request, 'view.html', { 'trip' : matchedTrip })
