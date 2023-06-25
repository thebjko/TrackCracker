from django.http import QueryDict
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy

from .forms import TaskForm
from .models import Task
from .utils import render, HttpResponse, HTTPResponseHXRedirect

def index(request):
    tasks = Task.objects.filter(supertask=None)
    context = {
        'tasks': tasks,
    }
    return render(request, 'crackers/index.html', context)


def tasks(request, pk):
    tasks = Task.objects.filter(supertask=pk)   # pk만 넘겨도 된다.
    context = {
        'tasks': tasks,
        'supertask': get_object_or_404(Task, pk=pk),
    }
    return render(request, 'crackers/task.html', context)


def create(request, pk=None):
    if request.method == 'POST':
        form  = TaskForm(data=request.POST)
        if form.is_valid():
            if pk is None:   # Objective를 생성하는 경우
                form.save()
                return redirect('tracks:index')
            task = form.save(commit=False)   # Subtask를 생성하는 경우
            task.supertask = get_object_or_404(Task, pk=pk)
            task.save()
            return redirect('tracks:tasks', pk)
    else:
        form = TaskForm()
    context = {
        'form': form,
        'supertask': pk,
    }
    return render(request, 'crackers/create.html', context)


def redirect_to_create(request, pk):
    return HTTPResponseHXRedirect(redirect_to=reverse_lazy('tracks:create', kwargs={'pk': pk}))


def detail(request, pk):
    context = {
        'task': get_object_or_404(Task, pk=pk)
    }
    trigger = {
        'change-offcanvas-title': {
            'title': context['task'].title
        }
    }
    return render(request, 'crackers/components/detail.html', context, trigger=trigger)


def update(request, pk):
    task = get_object_or_404(Task, pk=pk)
    if request.method == 'PUT':
        data = QueryDict(request.body).dict()
        form = TaskForm(data=data, instance=task)
        if form.is_valid():
            form.save()
            return HTTPResponseHXRedirect(redirect_to=reverse_lazy('tracks:tasks', kwargs={'pk': pk}))
    else:
        form = TaskForm(instance=task)
    context = {
        'form': form,
    }
    return render(request, 'crackers/update.html', context)