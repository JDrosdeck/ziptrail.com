from django import forms

class RegistrationForm(forms.Form):
    university = forms.CharField(label='Your University', required=True)
    email = forms.EmailField(label='Your school email',required=True) 
    passphrase = forms.CharField(label='Password', max_length=15, required=True, widget=forms.PasswordInput())
    passphraseCheck = forms.CharField(label='Verify password', max_length=15, required=True, widget=forms.PasswordInput())
 
    
class loginForm(forms.Form):
    email = forms.EmailField(label='Your school email', required=True)
    passphrase = forms.CharField(label='Password', max_length=15, required=True, widget=forms.PasswordInput())


