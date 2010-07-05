from django import forms

class SearchForm(forms.Form):
    university = forms.CharField(label='University to search rides for', required=False)
    zipCode = forms.CharField(label='Find rides near this Zip code', required=False)
    distance = forms.CharField(label = 'Distance from zip', required=False)
