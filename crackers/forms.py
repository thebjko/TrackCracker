from django import forms

from .models import Task

class TaskForm(forms.ModelForm):
    proportion = forms.IntegerField(required=True, label='비중')
    description = forms.CharField(required=False, label='설명')
    title = forms.CharField(required=True, label='태스크 제목')
    accumulative = forms.BooleanField(required=True, label=' 👈 서브태스크의 비중을 누적으로 입력하기 위해 체크하세요', widget=forms.CheckboxInput(attrs={'class': 'checkbox'}))

    class Meta:
        model = Task
        fields = (
            'title',
            'description',
            'proportion',
            'start',
            'accumulative',
        )

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
    
    
class TaskFormHelper(forms.Form):
    pass
