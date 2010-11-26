#This is where we are going to handle all of the common views
#like registering, login, logout.

from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.views.generic.simple import direct_to_template
from django.shortcuts import render_to_response
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from common.forms import RegistrationForm, loginForm
from myRides.models import Users, University
from geo.models import ZipCode

from django.contrib.sessions.models import Session
from django.utils import simplejson as json
from django.conf import settings
import types
from django.db import models
from django.core.serializers import serialize
from decimal import *

#Function takes in a queryset and will
#return a json object represeting that queryset
def generateUniversityJson(university):
    
    allSchools = dict()
    tempSchool = []
    for school in university:    
        tempSchool.append(school)
        allSchools['results'] = tempSchool 
    
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
                    return HttpResponseRedirect(settings.BASE_URL + '/rides/home/')
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


def isEmailDomainValid(request):
    if request.method == 'GET':
        email = request.GET.get('email', '')
        if email != '':

            emailDomains = University.objects.filter(email__iexact=email)
            Json = ([{'school' : x.name} for x in emailDomains])
            return HttpResponse(json.dumps(Json))


def register(request):

    if request.method == 'POST':
        print 'here'
        print request.POST
        form = RegistrationForm(request.POST)
        if form.is_valid():
            print 'here'
            email = form.cleaned_data['email']
            passphrase = form.cleaned_data['passphrase']
                       
            #make sure the useremail dosen't exist
            dbUsers = User.objects.filter(username=email)
            if len(dbUsers) == 0:
               
                #Get the domain of the email
                emailDomain = email[email.find('@'):]
               
                #Get the unvisity that has that email domain
                #create the passenger (everyone gets defaulted to a passenger)
                
                #emailDomains = StudentEmail.objects.get(email__iexact=emailDomain)    
                university = University.objects.filter(email__iexact=emailDomain)
                
                #TODO: If we get more then one university returned we then need 
                # to have the user select which school that they belong to.
                # if no school is returned then we need to have then input
                # their school and have it email us.
                if university.count() < 1:
                    return HttpResponse('School not found')
                elif university.count() > 1:
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
                return HttpResponseRedirect(settings.BASE_URL + '/rides/home/')
            else:

                form = RegistrationForm()
                return direct_to_template(request, 'register.html', { 'nameError' : True, 'form' : form })

        else:
            print 'form not valid'
            print form.errors

    elif request.method == 'GET':
        email = request.GET.get('email', '')
        password = request.GET.get('password','')
        
        # This extra value is used in the case that the university
        # the user belongs to is not distinct to the email address. This id 
        # represents the id of the university
        id = request.GET.get('id', '')
        
        if email != '' and password != '':
            emailDomain = email[email.find('@'):]
            #emailDomains = StudentEmail.objects.get(email__iexact=emailDomain)
            university = University.objects.filter(email__iexact=emailDomains)
            if university.count() < 1:
                return HttpResponse('School not found')
            elif university.count() > 1:
                #If there was no id given, then we should return the possible values back
                if id == '':
                    results = generateUniversityJson(university.values())
                    return HttpResponse(results)

                #We were given an id, and that should represent the university
                else:
                    university = University.objects.filter(id=id)

            user = User.objects.create_user(email,email,password)
            newUser = Users(user=user, university = university[0])
            newUser.save()
            user.is_staff = False
            user.save()
            user = authenticate(username=email, password=password)
            login(request, user)
            request.session['username']=email
            return HttpResponseRedirect(settings.BASE_URL + '/rides/home/')
            
        else:   
             form = RegistrationForm()
    return direct_to_template(request, 'register.html', { 'form' : form})

