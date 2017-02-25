from django import forms
from models import *

class UserAddForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = Users
        fields = ('name', 'email', 'password', 'role')

class UserLoginForm(forms.ModelForm):
    password = forms.CharField(required = False,widget=forms.PasswordInput)
    newuser = forms.BooleanField(required = False, initial = False)
    class Meta:
        model = Users
        fields = ('email', 'password','newuser')