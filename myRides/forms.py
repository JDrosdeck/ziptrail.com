from django import forms

class tripForm(forms.Form):
    startAddress = forms.CharField(label="Starting Address", required=True)
    endAddress = forms.CharField(label="Ending Address", required=True)
    leavingDate = forms.CharField(label="Date leaving", required=False)
    manufacturer = forms.CharField(label="Car Manufacturer", required = True)
    name = forms.CharField(label="Car Name", required=True)
    freeSeats = forms.CharField(label="Number of free seats", required=True)
    mpg = forms.CharField(label="Average MPG", required=False)

class waypointForm(forms.Form):
    startAddress = forms.CharField(label="Waypoint", required=False)
