from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic.simple import direct_to_template
from django.shortcuts import render_to_response
from django.contrib.sessions.models import Session
from django.conf import settings
from django.core.urlresolvers import reverse

#Database models                                       
from django.contrib.auth.models import User                                                                       
from myRides.models import Users, Trip, UsersTrip
from routes.models import Waypoint, Route, WaypointForm
from geo.models import Position
from badges.views import getBadges

#Forms                                                                                                                     
from django import forms
from myRides.forms import waypointForm

import ziptrailUtils

def create_waypoint_view(request):
    if request.method == 'GET':
        if request.user.is_authenticated:
            title = request.GET.get('title', '')
            address = request.GET.get('add','')
            lat = request.GET.get('lat','')
            lng = request.GET.get('lng','')
            
            if title and address and lat and lng:

                #Save the lat and lng
                pos, created  = Position.objects.get_or_create(latitude=float(lat),
                                                               longitude=float(lng))
                    
                #Create the waypoint
                waypoint, created  = Waypoint.objects.get_or_create(title=title, 
                                                                    waypoint=address, 
                                                                    lat_long=pos)
                
                #Add the waypoint to the list of users waypoints
                user = User.objects.get(username=request.session['username'])
                user = Users.objects.get(user=user)
                user.waypoints.add(waypoint)
                return HttpResponse('waypoint added')
                
            form = waypointForm()
            return direct_to_template(request, 
                                      'newWaypoint.html', 
                                      { 'form' : form 
                                        })

        return HttpResponse('not authenticated')
    
    elif request.method == 'POST':
        if request.user.is_authenticated:
            form = waypointForm(request.POST)
            if form.is_valid():
                title = form.cleaned_data['title']
                address = form.cleaned_data['address']
                lat = 0.0
                lng= 0.345

                pos, created = Position.objects.get_or_create(latitude=lat, 
                                                              longitude=lng)
                waypoint, created = Waypoint.objects.get_or_create(title=str(title), 
                                                                   waypoint=str(address), 
                                                                   lat_long=pos)
                    
                user = User.objects.get(username=request.session['username'])
                user = Users.objects.get(user=user)
                user.waypoints.add(waypoint)
                return HttpResponse('waypoint added')
    else:
        form = waypointForm()
        
    return direct_to_template(request, 
                              'newWaypoint.html', 
                              { 'form' : form 
                                })
