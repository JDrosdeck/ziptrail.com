from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.views.generic.simple import direct_to_template
from django.shortcuts import render_to_response
from django.contrib.sessions.models import Session
from django import forms
from django.contrib.auth.models import User
from django.db.models import Q


from search.forms import SearchForm
from geo.models import ZipCode
from routes.models import Route
from myRides.models import University, Trip, Users
from itertools import chain
import math
import operator


def search(request):

    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            
            #startPos and endPos are the lat/long for the address passed in via the form (javascript)
            startAddress = form.cleaned_data['startAddress']
            startLat = float(form.cleaned_data['startLat'])
            startLong = float(form.cleaned_data['startLong'])
            endAddress = form.cleaned_data['endAddress']
            endLat = float(form.cleaned_data['endLat'])
            endLong = float(form.cleaned_data['endLong'])
            distance = float(form.cleaned_data['distance'])
            results = runSearch(startAddress, startLat, startLong, endAddress, endLat, endLong, distance)
            
            query = reduce(operator.or_, (Q(pk=x) for x in results))
            results = Trip.objects.filter(query)
            
            return direct_to_template(request, 'search.html', { 'results': results, 'authenticated' : request.user.is_authenticated() })


    # handle the typical ajax search request
    elif request.method == 'GET':
        startAddress = request.GET.get('startAddress' ,'')
        startLat = request.GET.get('startLat', '')
        startLong = request.GET.get('startLong', '')
        endAddress = request.GET.get('endAddress' ,'')
        endLat = request.GET.get('endLat' ,'')
        endLong = request.GET.get('endLong', '')
        distance = request.GET.get('distance', '')
        results = runSearch(startAddress, startLat, startLong, endAddress, endLat, endLong, distance)

        query = reduce(operator.or_, (Q(pk=x) for x in results))
        results = Trip.objects.filter(query)
        
        return HttpResponse(results)

    else:
        form = SearchForm()
        return direct_to_template(request, 'search.html', { 'form' : form } )

def runSearch(startAddress,startLat, startLong, endAddress, endLat, endLong, distance, public=False):
    username = request.session['username']
    
    #Get the users information so we can extract out the university they belong to
    userInfo = Users.objects.get(user=User.objects.filter(username=username))

    #match all the rides being hosted by members of the university
    #public determins if it is only limited to university members
    matchedRides = Trip.objects.filter(host=Users.objects.filter(university=userInfo.university), public=public)
    
    #Determine which of those rides are beginning close to where you'd to start at
    # The default for now is 5 miles
    matches = calcDistances(matchedRides, startLat, startLong, 5)

    #Go through those matches and find any who will add a minimum time to the trip
    results = []
    for ride in matchedRides:
         for match in matches:
             if ride.id == match:
                #See if the end points are near
                 dist  = getDistance(endLong, ride.trip.endLat_Long.globalPos.longitude, endLat, ride.trip.endLat_Long.globalPos.latitude)
                 if dist < distance:
                     results.append(ride.id)
                 else:
                     #Check all the waypoints for nearby rides
                     for waypoint in ride.trip.waypoints.all():
                         if getDistance(endLong, waypoint.lat_long.longitude,endLat, waypoint.lat_long.latitude) < 10:
                             results.append(ride.id)
                        
                 if ride not in results:
                    #Do a psuedo average time to see if it won't make the trip much longer
                     pass
    return results

# calcDistances returns a list of the matching indicies of the given matchedRides.
# this way we are able to continue using the query object easily instead of 
# putting it back into a list
def calcDistances(matchedRides,lat, long,  distance):
    matches = []
    for ride in matchedRides:
        dist = getDistance(math.radians(long), math.radians(ride.trip.startLat_Long.globalPos.longitude), math.radians(lat), math.radians(ride.trip.startLat_Long.globalPos.latitude))
        if dist < int(distance):
            matches.append(ride.id)
    return matches

def getDistance(latStart, lngStart, latEnd, lngEnd):

    lngStart = math.radians(lngStart)
    lngEnd = math.radians(lngEnd)
    latStart = math.radians(latStart)
    latEnd = math.radians(latEnd)

    diff_long = lngEnd - lngStart
    diff_lat = latEnd - latStart

    a = (math.sin(diff_lat / 2))**2 + math.cos(latStart) * math.cos(latEnd) * (math.sin(diff_long / 2)) ** 2
    
    c = 2 * math.asin(min(1, math.sqrt(a)))
    dist = 3956 * c
    return dist

             
