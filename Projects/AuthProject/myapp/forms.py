from django import forms
from .models import *


class SignupForm(forms.ModelForm):
    class Meta:
        model=UserSignup
        fields='__all__'