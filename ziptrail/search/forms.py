from django import forms

class SearchForm(forms.Form):
    startAddress = forms.CharField(label='Starting near this Address', required=False)
    startCode = forms.CharField(label='Find rides starting near this zip', required=False)
    endAddress = forms.CharField(label='Ending near this Address', required=False)
    endCode = forms.CharField(label='Find rides ending near this Zip code', required=False)
    
    distance = forms.CharField(label = 'Distance from zip', required=False)
