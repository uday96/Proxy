from django import forms
from models import *

class CourseAddForm(forms.ModelForm):

    class Meta:
        model = Course
        fields = ('name', 'courseID','year', 'room')

class StudentAddForm(forms.Form):
    studentIDs = forms.CharField(required=True)

class UpdateAttendanceForm(forms.Form):
    #date = forms.DateField(required=True)
    courseID = forms.CharField(required=True)
    studentID = forms.CharField(required=True)
    CHOICES = (
       ("P", ("Present")),
       ("A", ("Absent")), 
   	)
    attendance = forms.ChoiceField(choices=CHOICES)
    