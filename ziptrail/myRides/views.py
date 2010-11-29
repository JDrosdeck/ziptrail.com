from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.views.generic.simple import direct_to_template
from django.shortcuts import render_to_response
from django.contrib.sessions.models import Session
from django import forms
from django.conf import settings
from django.utils import simplejson as json
from django.contrib.auth.models import User
from django.db.models import Q

#Database models
from myRides.models import Users, Trip, UsersTrip
from routes.models import Waypoint, Route, WaypointForm
from vehicle.models import Car
from geo.models import ZipCode, Position
from badges.views import getBadges

#Forms
from common.forms import loginForm
from myRides.forms import tripForm, waypointForm, joinTripForm

from search.views import getDistance
import datetime
import ziptrailUtils

# This is going to show a users home, and allow them to create a ride
# or join a ride
def home_View(request):

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
        pendingRides = Trip.objects.filter(pendingPassengers__user__id__exact=rider.id, active=True)
        
        #This gets all available rides exlcluding the user from being an acceptedPassenger, pendingPassenger or host
        # Basically any ride they have nothing to do with
        allRides = Trip.objects.filter(host__university=rider.university, active=True).exclude(acceptedPassengers__user__id__exact=rider.id).exclude(pendingPassengers__user__id__exact=rider.id).exclude(host=rider)

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
                    startLatLong, createdStart = Position.objects.get_or_create(latitude=latStart, longitude=lngStart)
                    endLatLong, createdEnd = Position.objects.get_or_create(latitude=latEnd, longitude=lngEnd)

                    #calculate the total miles
                    dist = getDistance(latStart,lngStart, latEnd, lngEnd)
                    print "DISTANCE " + str(dist)
                    gas = dist/16
                    route = Route(startAddress=startAddress, startZip=ZipCode.objects.get(zip=startZip), startLat_Long=startLatLong, endAddress=endAddress, endZip=ZipCode.objects.get(zip=endZip), endLat_Long=endLatLong, totalMiles=dist, gallonsGas=gas)
                    route.save()
                                                                   
                    #Create a new Trip, 
                    newRide = Trip(host=host, trip=route, public=public, customEndpoints=customEndpoints)
                    newRide.save()
                    return HttpResponseRedirect(settings.BASE_URL + '/rides/home')
                else:
                    return HttpResponse('Couldn\'t geocode')

        user = User.objects.get(username=request.session['username'])
        user = Users.objects.get(user=user)
               
        badges = getBadges(request)

        form = tripForm()
        return direct_to_template(request, 'home.html', { 'rides' : acceptedRides, 'form' : form, 'availableRides' : allRides, 'hostedRides' : HostedRides, 'userInfo': user, 'lst' : lst, 'badges' : badges })
    
    else:
        form = loginForm()
        return direct_to_template(request, 'login.html', { 'form' : form })


#This function allows for a user to create a new waypoint
def CreateNewWaypoint(request):
    if request.method == 'GET':
        if request.user.is_authenticated:
            title = request.GET.get('title', '')
            address = request.GET.get('add','')
            lat = request.GET.get('lat','')
            lng = request.GET.get('lng','')
            
            if title and address and lat and lng:

                #Save the lat and lng
                pos, created  = Position.objects.get_or_create(latitude=float(lat),longitude=float(lng))
                    
                #Create the waypoint
                waypoint, created  = Waypoint.objects.get_or_create(title=title, waypoint=address, lat_long=pos)
                
                #Add the waypoint to the list of users waypoints
                user = User.objects.get(username=request.session['username'])
                user = Users.objects.get(user=user)
                user.waypoints.add(waypoint)
                return HttpResponse('waypoint added')
                
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

                

                pos, created = Position.objects.get_or_create(latitude=lat, longitude=lng)
                waypoint, created = Waypoint.objects.get_or_create(title=str(title), waypoint=str(address), lat_long=pos)
                    
                user = User.objects.get(username=request.session['username'])
                user = Users.objects.get(user=user)
                user.waypoints.add(waypoint)
                return HttpResponse('waypoint added')
    else:
        form = waypointForm()
        
    return direct_to_template(request, 'newWaypoint.html', { 'form' : form })

    
def jsonifyResults(QuerySet):
    result = dict()
    tempResult = []
    for query in QuerySet:
        tempResult.append(query)
        result['results'] = tempResult
    return json.dumps(result)


#this function is for when a user wants to join a ride. They first need to ask permission from the host
# if they are allowed to join
def askToJoinRide(request):

    if request.method == 'POST':
        if request.user.is_authenticated:
            form = joinTripForm(request.POST, username=request.session['username'])
            if form.is_valid():
                tripId = form.cleaned_data['tripId']
                waypointId = form.cleaned_data['option']

                user = request.session['username']
                users = Users.objects.get(user__username=user)
                
                ridersTrip, created = UsersTrip.objects.get_or_create(user=users, waypoint=waypointId)
              
                # There were already some pending passengers, so here we make sure
                # that none of the pending passengers are the user trying to double
                # up their request                    
                
                #If this sql dosen't return a 0 we know the user is already in the trip
                isUserInTrip = (Q(id=tripId,pendingPassengers__waypoint__id__exact=ridersTrip.waypoint.id, pendingPassengers__user__id__exact=ridersTrip.user.id) | Q(id=tripId,acceptedPassengers__waypoint__id__exact=ridersTrip.waypoint.id, acceptedPassengers__user__id__exact=ridersTrip.user.id))
                    
                inTrip = Trip.objects.filter(isUserInTrip).count()
                   
                if inTrip != 0:
                    return HttpResponse('Your already a pending/accepted rider!')

                else:
                    trip = Trip.objects.get(id=tripId, active=True)
                    trip.pendingPassengers.add(ridersTrip)
                    trip.save()
                    return HttpResponse('You will be notified if you are accepted to the ride')
    else:
        return HttpResponse('wrong request type')


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
            
            tripId = request.GET.get('tripId', '')
            ridersTripId = request.GET.get('ridersTripId','')
            
            if tripId and ridersTripId:
                
                trip = Trip.objects.get(id=tripId)
                rider = UsersTrip.objects.get(id=ridersTripId)
                trip.acceptedPassengers.remove(rider)

                if rider.waypoint:
                    trip.trip.waypoints.remove(rider.waypoint)
                    trip.save()
                    return HttpResponse('Rider removed from trip')

            return HttpResponse('import args')
        return HttpResponse('not authenticated')
    return HttpResponse('wrong request type')

def cancelRide(request):
    if request.method == 'GET':
        if request.user.is_authenticated:
            #We need the id of the trip to remove
            tripId = request.GET.get('tripId','')
            
            if tripId:
                #Get the user
                user = User.objects.get(username=request.session['username'])
                rider = Users.objects.get(user=user)
                #Query for the trip
                try:
                    trip = Trip.objects.get(id=tripId, host=rider, active=True)
                    trip.active = False
                    trip.save()
                    return HttpResponse("Ride canceled")
                except:
                    return HttpResponse("error finding trip:Delete Ride")
                
                


#viewRide is where a rider is going to view the details of a ride. See all the information
#associated with it. And be able to compare the current map to a map of their ride added to the 
#the trip. They will be able to select any waypoint they have and ask the host to join the trip
def viewRide(request, tripId):
    # id represents the ID of the TRIP
    # We want to show detailed information about the trip
    # ie. google map. Waypoints, people involved
    
    matchedTrip = Trip.objects.get(id=tripId)

    #Check to see if the person requesting this ridde should even be able to see the ride
    user = User.objects.get(username=request.session['username'])
    rider = Users.objects.get(user=user)
    
    if (matchedTrip.host.university == rider.university) or (matchedTrip.public == True):
    
        #get the users waypointdata
        username = request.session['username']
        form = joinTripForm(initial={'tripId': tripId }, username=user.username)
        print form
        return direct_to_template(request, 'view.html', { 'trip' : matchedTrip, 'form' : form })
    else:
        return HttpResponse('Sorry thats a private ride')
