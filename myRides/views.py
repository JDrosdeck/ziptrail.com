from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.views.generic.simple import direct_to_template
from django.shortcuts import render_to_response
from django.contrib.sessions.models import Session
from django import forms
from django.conf import settings
from django.utils import simplejson as json

#Database models
from rideShare.myRides.models import Users, Trip, UsersTrip
from rideShare.routes.models import Waypoint, Route, WaypointForm
from rideShare.vehicle.models import Car
from rideShare.geo.models import ZipCode, Position


from rideShare.common.forms import loginForm
from rideShare.myRides.forms import tripForm, waypointForm, waypointsForm
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
        
        #This gets all available rides exlcluding the user from being an acceptedPassenger, pendingPassenger or host
        # Basically any ride they have nothing to do with
        allRides = Trip.objects.filter().exclude(acceptedPassengers__id__exact=rider).exclude(pendingPassengers__id__exact=rider).exclude(host=rider)

        #All the rides that the user is hosting
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
         


        user = User.objects.get(username=request.session['username'])
        user = Users.objects.get(user=user)
        
    
        test = Users.objects.get(user = User.objects.get(username=request.session['username']))
        test1 = test.waypoints.all()

        userName = request.session['username']
        form = waypointsForm(username=userName)
        form1 = waypointsForm(username=request.session['username'])
        return direct_to_template(request, 'home.html', { 'rides' : acceptedRides, 'form' : form, 'availableRides' : allRides, 'hostedRides' : HostedRides, 'user':user, 'trip1': form1})
    
    else:
        form = loginForm()
        return direct_to_template(request, 'login.html', { 'form' : form })


#This function allows for a user to create a new waypoint
def CreateNewWaypoint(request):
    if request.method == 'GET':
        if request.user.is_authenticated:
            title = request.GET.get('title', '')
            address = request.GET.get('address','')
            lat = request.GET.get('lat','')
            lng = request.GET.get('lng','')
            
            if title and address and lat and lng:
#                try:
                    #Save the lat and lng
                pos = Position.objects.get_or_create(latitude=float(lat),longitude=float(lng))
                    
                    #Create the waypoint
                waypoint = Waypoint.objects.get_or_create(title=title, waypoint=address, lat_long=pos)
                
                    #Add the waypoint to the list of users waypoints
                user = User.objects.get(username=request.session['username'])
                user = Users.objects.get(user=user)
                user.waypoints.add(waypoint)
                return HttpResponse('waypoint added')
                #except:
                #    return HttpResponse('waypoint not added')
            
            form = waypointForm()
            return direct_to_template(request, 'newWaypoint.html', { 'form' : form })

        return HttpResponse('not authenticated')
    
    elif request.method == 'POST':
        if request.user.is_authenticated:
            form = waypointForm(request.POST)
            if form.is_valid():
                title = form.cleaned_data['title']
                address = form.cleaned_data['address']
                lat = 0.0
                lng= 0.345

                try:
                    pos = Position.objects.get(latitude=lat, longitude=lng)
                
                except:
                    pos = Position(latitude=lat, longitude=lng)
                    pos.save()
                    pos = Position.objects.get(latitude=lat, longitude=lng)
                    print pos
                
                try:
                    waypoint = Waypoint.objects.get(title=str(title), waypoint=str(address), lat_long=pos)
                except:
                    waypoint = Waypoint(title=str(title), waypoint=str(address), lat_long=pos)
                    waypoint.save()

                user = User.objects.get(username=request.session['username'])
                user = Users.objects.get(user=user)
                user.waypoints.add(waypoint)
                return HttpResponse('waypoint added')
                #except:
                #    return HttpResponse('waypoint not added')
    else:
        form = waypointForm()
        
    return direct_to_template(request, 'newWaypoint.html', { 'form' : form })

    



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
            wayPointId = request.GET.get('wayPointId', '')
            
            user = request.session['username']

            #check for proper input
            if tripId and user:
                
                try:
                    #Try and get the trip based on the tripId given
                    trip = Trip.objects.get(id=tripId)
                    
                    #Based on the waypoint ID and the user. check to see if the info already
                    # exists in UsersTrip
                    #First get the user
                    user = User.objects.get(username=user)
                    users = Users.objects.get(user=user)
                    #Get the id of the UsersTrip
                    
                    ridersTrip = UsersTrip.objects.get_or_create(user=users, waypoint=wayPointId)
                    #Add the rider to the pending riders list for review
                    trip.pendingPassengers.add(ridersTrip)
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
            #We need the id of the ridersTrip to add to the trip.
            ridersTripId = request.GET.get('ridersTripId','')

            
            if tripId and ridersTripId:
               try:
                   #Get the trip
                   trip = Trip.objects.get(id=tripId)
                   ridersTrip = UsersTrip.objects.get(id=ridersTripId)
                
                   trip.acceptedPassengers.add(ridersTrip)
                   trip.pendingPassengers.remove(ridersTrip)

                   if ridersTrip.waypoint:
                       trip.trip.waypoints.add(ridersTrip.waypoint)
                   trip.save()
                   return HttpResponse('Rider added to trip, pending rider removed')
               except:
                   return HttpResponse('')
            return HttpResponse('import args')
        return HttpResponse('not authenticated')
    return HttpResponse('wrong request type')
            

def removeRiderFromRide(request):
    if request.method == 'GET':
        if request.user.is_authenticated:
                #we need the id of the Trip to add the user to                                                                                          
            tripId = request.GET.get('tripId', '')

            ridersTripId = request.GET.get('ridersTripId','')
            

            if tripId and ridersTripId:
                try:
                   #Get the trip                                                                                                                   
                    trip = Trip.objects.get(id=tripId)
                    rider = UsersTrip.objects.get(id=ridersTripId)

                    trip.acceptedPassengers.remove(rider)
                    if rider.waypoint:
                        trip.trip.waypoints.remove(rider.waypoint)
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
