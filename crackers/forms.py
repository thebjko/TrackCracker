from django import forms

from .models import Objective

class ObjectiveForm(forms.ModelForm):
    
    class Meta:
        model = Objective
        fields = '__all__'
