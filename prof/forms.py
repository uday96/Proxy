from django import forms
from models import *

# class UserAddForm(forms.ModelForm):
#     password = forms.CharField(widget=forms.PasswordInput)

#     class Meta:
#         model = Users
#         fields = ('name','ID','deptID', 'email', 'password', 'role')

class CourseAddForm(forms.ModelForm):
    # password = forms.CharField(required = False,widget=forms.PasswordInput)
    # newuser = forms.BooleanField(required = False, initial = False)
    class Meta:
        model = Course
        fields = ('name', 'courseID','year', 'room')

class StudentAddForm(forms.Form):
    studentIDs = forms.CharField(required=True)