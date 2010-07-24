from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.views.generic.simple import direct_to_template
from django.shortcuts import render_to_response
from django.contrib.sessions.models import Session
from django import forms
from django.contrib.auth.models import User
from django.db.models import Q


from rideShare.search.forms import SearchForm
from rideShare.zip.models import ZipCode
from rideShare.routes.models import Route
from rideShare.myRides.models import University, Trip, Users
from itertools import chain
import math
import operator


def search(request):

    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            
            #Grab the users university
            username = request.session['username']
            
            userInfo = Users.objects.get(user=User.objects.filter(username=username))

            endCode = form.cleaned_data['endCode']
            startCode = form.cleaned_data['startCode']
            distance = form.cleaned_data['distance']
            
            # Get all the rides that are matched for that university
            matchedRides = Trip.objects.filter(host=Users.objects.filter(university=userInfo.university), public=False)


            endzip = ZipCode.objects.get(zip=endCode)
            startzip = ZipCode.objects.get(zip=startCode)

            #Find all the rides that are starting close to where you want to start from
            nearbyRides = calcDistances(matchedRides, startzip, 5)
            print nearbyRides


            #get all the waypoints associated wth that university
            results = []

            for x in nearbyRides:
                for ride in matchedRides:
                    if ride.id == x:
                        #calculate the distance of the end point
                        if getDistance(endzip.longitude, ride.trip.endZip.globalPos.longitude, endzip.latitude, ride.trip.endZip.globalPos.latitude) < distance:
                            print 'added to results'
                            results.append(ride)
                            break
                        else:
                            for waypoint in ride.trip.waypoints.all():
                                if getDistance(endzip.longitude, waypoint.zipCode.lat_long.longitude, endzip.latitude, waypoint.zipCode.lat_long.latitude) < distance:
                                    results.append(ride)
                                    break
                    
                
                           
            matches = results                       
           # matches = calcDistances(matchedRides, zip, distance)
            
            return direct_to_template(request, 'search.html', { 'results': matches, 'authenticated' : request.user.is_authenticated() })


    # handle the typical ajax search request
    elif request.method == 'GET':
        None



        form = SearchForm()
        return direct_to_template(request, 'search.html', { 'form' : form } )



def calcDistances(matchedRides,zip, distance):
    matches = []
    for ride in matchedRides:
        dist = getDistance(math.radians(float(zip.longitude)), math.radians(float(ride.trip.startZip.globalPos.longitude)), math.radians(float(zip.latitude)), math.radians(float(ride.trip.startZip.globalPos.latitude)))
        if dist < int(distance):
            matches.append(ride.id)
    return matches




def getDistance(long1, long2, lat1, lat2):

    diff_long = long2 - long1
    diff_lat = lat2 - lat1

    a = (math.sin(diff_lat / 2))**2 + math.cos(lat1) * math.cos(lat2) * (math.sin(diff_long / 2)) ** 2
    
    c = 2 * math.asin(min(1, math.sqrt(a)))
    dist = 3956 * c
    return dist

             
