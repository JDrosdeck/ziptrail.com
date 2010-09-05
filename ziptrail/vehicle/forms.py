from django import forms

class vehicleForm(forms.Form):
    freeSeats = forms.CharField(label="Number of free seats", required=True)

