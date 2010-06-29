from django import forms

class tripForm(forms.Form):
    startAddress = forms.CharField(label="Starting Address", required=True)
    endAddress = forms.CharField(label="Ending Address", required=True)
    leavingDate = forms.CharField(label="Date leaving", required=False)
    freeSeats = forms.CharField(label="Number of free seats", required=True)

class waypointForm(forms.Form):
    startAddress = forms.CharField(label="Waypoint", required=False)
