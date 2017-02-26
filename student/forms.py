from django import forms
from models import *

class RaiseQueryForm(forms.ModelForm):
    query = forms.CharField( widget=forms.Textarea )
    class Meta:
        model = Queries
        fields = ('studentID','courseID','query')