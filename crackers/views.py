from django.http import QueryDict
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy, resolve

from .forms import TaskForm, ObjectiveForm
from .models import Task, Objective
from .utils import render, HttpResponse, HTTPResponseHXRedirect

def index(request):
    objectives = Objective.objects.all()
    context = {
        'objectives': objectives,
    }
    return render(request, 'crackers/index.html', context)


def tasks(request, objective_pk):
    tasks = Task.objects.filter(objective=objective_pk, supertask=None)   # pk만 넘겨도 된다.
    context = {
        'tasks': tasks,
        'objective': get_object_or_404(Objective, pk=objective_pk),
        'base_template': 'crackers/base/_task_base.html',
    }
    return render(request, 'crackers/task.html', context)


def subtasks(request, supertask_pk):
    tasks = Task.objects.filter(supertask=supertask_pk)
    context = {
        'tasks': tasks,
        'supertask': get_object_or_404(Task, pk=supertask_pk),
        'base_template': 'crackers/base/_subtask_base.html',
    }
    return render(request, 'crackers/task.html', context)


# create objective
def create(request):
    if request.method == 'POST':
        form = ObjectiveForm(data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('tracks:index')
    else:
        form = ObjectiveForm()
    context = {
        'form': form,
        'title': 'Create Objective',
        'action': reverse_lazy('tracks:create')
    }
    return render(request, 'crackers/create.html', context)


# create task (*task : subtask right under an objective)
def create_task(request, objective_pk):   
    if request.method == 'POST':
        form = TaskForm(data=request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.objective = get_object_or_404(Objective, pk=objective_pk)
            task.save()
            return redirect('tracks:tasks', objective_pk)
    else:
        form = TaskForm()
    context = {
        'form': form,
        'objective_pk': objective_pk,
        'title': 'Create Task',
        'action': reverse_lazy('tracks:create_task', kwargs={'objective_pk': objective_pk})
    }
    return render(request, 'crackers/create.html', context)


def create_subtask(request, supertask_pk):
    if request.method == 'POST':
        form = TaskForm(data=request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.supertask = get_object_or_404(Task, pk=supertask_pk)
            task.objective = task.supertask.objective
            task.save()
            return redirect('tracks:subtasks', supertask_pk)
    else:
        form = TaskForm()
    context = {
        'form': form,
        'supertask_pk': supertask_pk,
        'title': 'Create Task',
        'action': reverse_lazy('tracks:create_subtask', kwargs={'supertask_pk': supertask_pk})
    }
    return render(request, 'crackers/create.html', context)


def detail(request, objective_pk):
    context = {
        'objective': get_object_or_404(Objective, pk=objective_pk)
    }
    trigger = {
        'change-offcanvas-title': {
            'title': context['objective'].title
        }
    }
    return render(request, 'crackers/components/detail.html', context, trigger=trigger)


def task_detail(request, supertask_pk):
    context = {
        'task': get_object_or_404(Task, pk=supertask_pk)
    }
    trigger = {
        'change-offcanvas-title': {
            'title': context['task'].title
        }
    }
    return render(request, 'crackers/components/task_detail.html', context, trigger=trigger)


def update(request, objective_pk):   # Objective Update
    objective = get_object_or_404(Objective, pk=objective_pk)
    if request.method == 'PUT':
        data = QueryDict(request.body).dict()
        form = ObjectiveForm(data=data, instance=objective)
        if form.is_valid():
            form.save()
            # 적절하게 분배
            return redirect(request.META.get('HTTP_REFERER'))
    else:
        form = ObjectiveForm(instance=objective)
    context = {
        'form': form,
        'title': 'Update Objective',
    }
    return render(request, 'crackers/update.html', context)


def update_task(request, task_pk):
    task = get_object_or_404(Task, pk=task_pk)
    if request.method == 'PUT':
        data = QueryDict(request.body).dict()
        form = TaskForm(data=data, instance=task)
        if form.is_valid():
            form.save()
            if task.supertask is None:
                redirect_to = reverse_lazy('tracks:tasks', kwargs={'objective_pk': task.objective.pk})
            else:
                redirect_to = reverse_lazy('tracks:subtasks', kwargs={'supertask_pk': task.supertask.pk})
            return HTTPResponseHXRedirect(redirect_to=redirect_to)
    else:
        form = TaskForm(instance=task)
    context = {
        'form': form,
        'title': 'Update Task',
    }
    return render(request, 'crackers/update.html', context)


def delete(request, objective_pk):
    objective = get_object_or_404(Objective, pk=objective_pk)
    objective.delete()
    # redirect시 trigger에 대한 코드 실행 후 페이지가 바뀐다. 어떻게 유지할까
    return HTTPResponseHXRedirect(redirect_to=reverse_lazy('tracks:index'))

