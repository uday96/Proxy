from django import forms
from models import *

class UserAddForm(forms.ModelForm):
    password = forms.CharField(required = True,widget=forms.PasswordInput)
    class Meta:
        model = Users
        fields = ('name','ID','deptID', 'email', 'password', 'role')

class UserLoginForm(forms.ModelForm):
    password = forms.CharField(required = True,widget=forms.PasswordInput)
    class Meta:
        model = Users
        fields = ('email', 'password')