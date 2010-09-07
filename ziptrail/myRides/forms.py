from django import forms
from django.forms import ModelForm
from myRides.models import Users, User
from routes.models import Waypoint



class joinTripForm(forms.Form):

     option = forms.ModelChoiceField(queryset = Waypoint.objects.none())
     tripId = forms.IntegerField(widget=forms.HiddenInput())
     
     def __init__(self, *args, **kwargs):
                    
          username = kwargs['username']
          del kwargs['username']
          super(joinTripForm, self).__init__(*args, **kwargs)
          self.fields["option"].queryset =  Users.objects.get(user = User.objects.get(username=username)).waypoints.all()
          

class waypointForm(forms.Form):
    title = forms.CharField(label="Name of waypoint", required=True)
    address  = forms.CharField(label="Address to stop at", required=True)
    


class tripForm(forms.Form):
    startAddress = forms.CharField(label="Starting Address", required=True)
    startZip = forms.CharField(label="Starting Zip Code", required=True)
    endAddress = forms.CharField(label="Ending Address", required=True)
    endZip = forms.CharField(label="Ending Zip Code", required=True)
    leavingDate = forms.CharField(label="Date leaving", required=False)
    public = forms.BooleanField(label="Allow anyone to view this ride", widget=forms.CheckboxInput, required=False)
    customEndpoints = forms.BooleanField(label="Allow custom stops", widget=forms.CheckboxInput, required=False)
    freeSeats = forms.ChoiceField(widget=forms.Select(), choices=([('1', '1'), ('2', '2'), ('3','3'), ('4', '4'), ('5', '5')]), label='Number of Free seats?', required=True)
