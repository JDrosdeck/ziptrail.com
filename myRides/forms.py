from django import forms

class tripForm(forms.Form):
    startAddress = forms.CharField(label="Starting Address", required=True)
    startZip = forms.CharField(label="Starting Zip Code", required=True)
    endAddress = forms.CharField(label="Ending Address", required=True)
    endZip = forms.CharField(label="Ending Zip Code", required=True)
    leavingDate = forms.CharField(label="Date leaving", required=False)
    freeSeats = forms.ChoiceField(widget=forms.Select(), choices=([('1', '1'), ('2', '2'), ('3','3'), ('4', '4'), ('5', '5')]), label='Number of Free seats?', required=True)
class waypointForm(forms.Form):
    startAddress = forms.CharField(label="Waypoint", required=False)
