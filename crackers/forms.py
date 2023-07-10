from django import forms

from .models import Task

class TaskForm(forms.ModelForm):
    proportion = forms.IntegerField(required=True, label='Weight')
    description = forms.CharField(required=False, label='Description')
    title = forms.CharField(required=True, label='Task Title')
    accumulative = forms.BooleanField(required=False, label=' 👈 Check to have your subtasks\' weight accumulated', widget=forms.CheckboxInput(attrs={'class': 'checkbox'}))

    class Meta:
        model = Task
        fields = (
            'title',
            'description',
            'proportion',
            'start',
            'accumulative',
        )
