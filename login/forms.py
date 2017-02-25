from django import forms
from models import *

class UserAddForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = Users
        fields = ('name', 'email', 'password', 'role')