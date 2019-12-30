from django import forms
class LoginForm(forms.Form):
    username = forms.CharField(max_length=128)
    password = forms.CharField(max_length=256)

class RegisterForm(forms.Form):
    username = forms.CharField(max_length=128)
    password1 = forms.CharField(max_length=256)
    password2 = forms.CharField(max_length=256)
    email = forms.CharField(max_length=128)

class WorkForm(forms.Form):
    workname = forms.CharField()
    date = forms.CharField()
    carrier = forms.CharField()
    introduction = forms.CharField()
