from django import forms

class SearchForm(forms.Form):
    startCode = forms.CharField(label='Find rides starting near this zip', required=False)
    endCode = forms.CharField(label='Find rides ending near this Zip code', required=False)
    
    distance = forms.CharField(label = 'Distance from zip', required=False)
