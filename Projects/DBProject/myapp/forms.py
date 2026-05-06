from django import forms
from .models import *

class Studform(forms.ModelForm):
    class Meta:
        model=Studinfo
        fields='__all__'