from django import forms

class RegistrationForm(forms.Form):
    email = forms.CharField(max_length=25, required=True) 
    passphrase = forms.CharField( max_length=15, required=True)
    passphraseCheck = forms.CharField(max_length=15, required=True)
 
    
class loginForm(forms.Form):
    email = forms.EmailField(label='Your school email', required=True)
    passphrase = forms.CharField(label='Password', max_length=15, required=True, widget=forms.PasswordInput())


