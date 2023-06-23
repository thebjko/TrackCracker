from django.shortcuts import render, redirect
from django.urls import reverse_lazy

from .forms import TaskForm
from .models import Task
from .utils import HTTPResponseHXRedirect

def index(request):
    tasks = Task.objects.filter(supertask=None)
    context = {
        'tasks': tasks,
    }
    return render(request, 'crackers/index.html', context)


def create(request):
    if request.method == 'POST':
        form  = TaskForm(data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('tracks:index')
    else:
        form = TaskForm()
    context = {
        'form': form,
    }
    return render(request, 'crackers/objectives/create.html', context)

def redirect_to_tasks(request, pk):
    '''for hx-get to redirect'''
    return HTTPResponseHXRedirect(redirect_to=reverse_lazy('tracks:tasks', kwargs={'pk': pk}))


def tasks(request, pk):
    return render(request,)