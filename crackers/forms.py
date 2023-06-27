from django import forms
from django.core.exceptions import ValidationError
from django.forms.utils import ErrorList

from .models import Task, Objective

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = (
            'title',
            'description',
            'type',
            'proportion',
            'total',
        )
    
    def clean_proportion(self):
        proportion = self.cleaned_data.get('proportion')
        supertask = self.cleaned_data.get('supertask')
        if supertask is None and proportion is None:
            return 10_000
        elif supertask is not None and proportion is None:
            self._errors['proportion'] = ErrorList(["Proportion is required when supertask is not None."])
            raise ValidationError("Proportion is required when supertask is not None.")
        return proportion

    
class TaskFormHelper(forms.Form):
    pass


class ObjectiveForm(forms.ModelForm):
    
    class Meta:
        model = Objective
        fields = (
            'title',
            'description',
            'type',
            'total',
        )
