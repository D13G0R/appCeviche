from django import forms

class LoginForm(forms.Form):
    username = forms.CharField(max_length=40)
    password = forms.CharField(max_length=80, widget=forms.PasswordInput(), required=True)