from django import forms
from django.core.exceptions import ValidationError
from django.forms.utils import ErrorList

from .models import Task

class TaskForm(forms.ModelForm):
    # accumulative = forms.CheckboxInput(widge)
    class Meta:
        model = Task
        fields = (
            'title',
            'description',
            'proportion',
            # 'accumulative',
        )
    
    # def clean_proportion(self):
    #     proportion = self.cleaned_data.get('proportion')
    #     supertask = self.cleaned_data.get('supertask')
    #     if supertask is None and proportion is None:
    #         return 10_000
    #     elif supertask is not None and proportion is None:
    #         self._errors['proportion'] = ErrorList(["Proportion is required when supertask is not None."])
    #         raise ValidationError("Proportion is required when supertask is not None.")
    #     return proportion

    
class TaskFormHelper(forms.Form):
    pass

