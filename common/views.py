#This is where we are going to handle all of the common views
#like registering, login, logout.

from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.views.generic.simple import direct_to_template
from django.shortcuts import render_to_response
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from rideShare.common.forms import RegistrationForm, loginForm
from rideShare.myRides.models import Users, University, StudentEmail
from rideShare.zip.models import ZipCode

from django.contrib.sessions.models import Session
from django.utils import simplejson as json
import types
from django.db import models
from django.core.serializers import serialize
from decimal import *

#Function takes in a queryset and will
#return a json object represeting that queryset
def generateUniversityJson(university):
    print '-----------------------'
    
    allSchools = dict()
    tempSchool = []
    for school in university:    
        tempSchool.append(school)
        allSchools['results'] = tempSchool 
    
    print '----------------------'

    return json.dumps(allSchools)

def login_View(request):

    if request.method == 'POST':
        form = loginForm(request.POST)
        
        if form.is_valid():
            email = form.cleaned_data['email']
            passphrase = form.cleaned_data['passphrase']
            user = authenticate(username=email, password=passphrase)
            if user is not None:
                if user.is_active:
                    #direct to home
                    login(request, user)
                    request.session['username'] = email
                    return HttpResponseRedirect('/rides/home/')
                else:
                    return HttpResponse("Your account has been disabled")
            else:
                return HttpResponse("Your username and password are incorrect")
    else:
        form = loginForm()
    return direct_to_template(request, 'login.html', { 'form' : form })
            
def logout_View(request):
    logout(request)
    return HttpResponse("Logged Out")


def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            passphrase = form.cleaned_data['passphrase']
                       
            #make sure the useremail dosen't exist
            dbUsers = User.objects.filter(username=email)
            if len(dbUsers) == 0:
               
                #Get the domain of the email
                emailDomain = email[email.find('@'):]
               
                #Get the unvisity that has that email domain
                #create the passenger (everyone gets defaulted to a passenger)
                
                emailDomains = StudentEmail.objects.get(email__iexact=emailDomain)
                university = University.objects.filter(email__id__exact=emailDomains.id)
                
                #TODO: If we get more then one university returned we then need 
                # to have the user select which school that they belong to.
                # if no school is returned then we need to have then input
                # their school and have it email us.
                print 'count: ' + str(university.count())
                if university.count() < 1:
                    return HttpResponse('School not found')
                elif university.count() > 1:
                    print university.count()
                    # The internal json serializes gives us way too much
                    # information that we don't need so we need a custom 
                    # function to go thorugh and generate the proper json
                    # return
                    results = generateUniversityJson(university.values())
                    return HttpResponse(results)
               
                # create the user
                user = User.objects.create_user(email,email,passphrase)
                

                newUser = Users(user=user, university = university[0])
                newUser.save()
                user.is_staff = False
                user.save()
                user = authenticate(username=email, password=passphrase)
                login(request, user)
                request.session['username'] = email
                return HttpResponseRedirect('/rides/home/')
            else:
                form = RegistrationForm()
                return direct_to_template(request, 'register.html', { 'nameError' : True, 'form' : form })

    elif request.method == 'GET':
        email = request.GET.get('email', '')
        password = request.GET.get('password','')
        print email
        print password
        
        if email != '' and password != '':
            emailDomain = email[email.find('@'):]
            emailDomains = StudentEmail.objects.get(email__iexact=emailDomain)
            university = University.objects.filter(email__id__exact=emailDomains.id)
            if university.count() < 1:
                return HttpResponse('School not found')
            elif university.count() > 1:
                results = generateUniversityJson(university.values())
                return HttpResponse(results)

            user = User.objects.create_user(email,email,password)
            newUser = Users(user=user, university = university[0])
            newUser.save()
            user.is_staff = False
            user.save()
            user = authenticate(username=email, password=password)
            login(request, user)
            request.session['username']=email
            return HttpResponseRedirect('/rides/home/')
            
        else:   
             form = RegistrationForm()
    return direct_to_template(request, 'register.html', { 'form' : form})

