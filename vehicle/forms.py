from django import forms

class vehicleForm(forms.Form):
    manufacturer = forms.CharField(label="Car Manufacturer", required = True)
    name = forms.CharField(label="Car Name", required=True)
    freeSeats = forms.CharField(label="Number of free seats", required=True)
    mpg = forms.CharField(label="Average MPG", requred=False)
