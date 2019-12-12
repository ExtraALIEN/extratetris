from django import forms

class SignupForm(forms.Form):
    username = forms.CharField(max_length=20)
    email = forms.EmailField(max_length=30)
    password = forms.CharField(max_length=20, widget=forms.PasswordInput)
