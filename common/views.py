#This is where we are going to handle all of the common views
#like registering, login, logout.

from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.views.generic.simple import direct_to_template
from django.shortcuts import render_to_response
from django import forms
from django.contrib.auth.models import User
from rideShare.common.forms import RegistrationForm, loginForm
from rideShare.myRides.models import Passenger, University

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            passphrase = form.cleaned_data['passphrase']
            university = form.cleaned_data['university']
            
            #make sure the useremail dosen't exist
            dbUsers = User.objects.filter(username=email)
            if len(dbUsers) == 0:
                #create the user
                user = User.objects.create_user(email, email, passphrase)
                #create the passenger (everyone gets defaulted to a passenger)
                university = University(name=university)
                university.save()
                passenger = Passenger(user=user, university=university)
                passenger.save()
                user.is_staff = False
                user.save()
            else:
                form = RegistrationForm()
                return direct_to_template(request, 'register.html', { 'nameError' : True, 'form' : form })

    else:
        form = RegistrationForm()
    return direct_to_template(request, 'register.html', { 'form' : form})
