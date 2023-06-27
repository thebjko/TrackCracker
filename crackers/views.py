from django.http import QueryDict
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy

from .forms import TaskForm, ObjectiveForm
from .models import Task, Objective
from .utils import render, HttpResponse, HTTPResponseHXRedirect

def index(request):
    objectives = Objective.objects.all()
    context = {
        'objectives': objectives,
    }
    return render(request, 'crackers/index.html', context)


def tasks(request, pk):
    tasks = Task.objects.filter(objective=pk)   # pk만 넘겨도 된다.
    context = {
        'tasks': tasks,
        'objective': get_object_or_404(Objective, pk=pk),
    }
    return render(request, 'crackers/task.html', context)


# create objective
def create(request, pk=None):
    if request.method == 'POST':
        form = ObjectiveForm(data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('tracks:index')
    else:
        form = ObjectiveForm()
    context = {
        'form': form,
    }
    return render(request, 'crackers/create.html', context)


# create task (*task : subtask right under an objective)
def create_task(request, pk):   
    if request.method == 'POST':
        form = TaskForm(data=request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.objective = get_object_or_404(Objective, pk=pk)
            task.save()
            return redirect('tracks:tasks', pk)
    else:
        form = TaskForm()
    context = {
        'form': form,
        'objective_pk': pk,
    }
    return render(request, 'crackers/create_task.html', context)


def redirect_to_create_task(request, pk):
    return HTTPResponseHXRedirect(redirect_to=reverse_lazy('tracks:create_task', kwargs={'pk': pk}))


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


def delete(request, pk):
    task = get_object_or_404(Task, pk=pk)
    supertask = task.supertask
    task.delete()
    if supertask is None:
        redirect_to = reverse_lazy('tracks:index')
    else:
        redirect_to = reverse_lazy('tracks:tasks', kwargs={'pk': supertask.pk})
    # redirect시 trigger에 대한 코드 실행 후 페이지가 바뀐다.
    # return HttpResponse(trigger={'test': dict()})
    return HTTPResponseHXRedirect(redirect_to=redirect_to)
