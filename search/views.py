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
import math
import operator

def search(request):

    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            university = form.cleaned_data['university']
            zipcode = form.cleaned_data['zipCode']
            distance = form.cleaned_data['distance']
            
                # get all the trips listed for the university
            matchedUniversity = University.objects.get(name__iexact=university)
            
                # Get all the rides that are matched for that university
            matchedRides = Trip.objects.filter(host=Users.objects.filter(university=matchedUniversity))
            print len(matchedRides)

                # Get the zip object passe in through the form
            zip = ZipCode.objects.get(zip=zipcode)

            matches = []
            for ride in matchedRides:
                dist = getDistance(math.radians(float(zip.longitude)), math.radians(float(ride.trip.startZip.longitude)), math.radians(float(zip.latitude)), math.radians(float(ride.trip.startZip.latitude)))
                if dist < int(distance):
                    matches.append(Q(zip=ride.trip.startZip.zip))
                    print dist
            #get the trip informations with the found zip codes
            #print Trip.objects.filter(trip=Route.objects.filter(startZip=ZipCode.objects.filter(reduce(operator.or_, matches)))).count()

            print ZipCode.objects.filter(reduce(operator.or_, matches)).count()
            
            return direct_to_template(request, 'search.html', { 'results': matches })
            



    else:
        form = SearchForm()
        return direct_to_template(request, 'search.html', { 'form' : form } )

def getDistance(long1, long2, lat1, lat2):

    diff_long = long2 - long1
    diff_lat = lat2 - lat1

    a = (math.sin(diff_lat / 2))**2 + math.cos(lat1) * math.cos(lat2) * (math.sin(diff_long / 2)) ** 2
    
    c = 2 * math.asin(min(1, math.sqrt(a)))
    dist = 3956 * c
    return dist

             
