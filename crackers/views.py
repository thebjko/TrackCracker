from django.http import QueryDict
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy, resolve

from .forms import TaskForm
from .models import Task
from .utils import render, HttpResponse, HTTPResponseHXRedirect

def index(request):
    tasks = Task.objects.filter(supertask=None)
    context = {
        'tasks': tasks,
        'base_template': 'crackers/base/_objective.html',
    }
    return render(request, 'crackers/index.html', context)


def tasks(request, supertask_pk):
    tasks = Task.objects.filter(supertask=supertask_pk)   # pk만 넘겨도 된다.
    supertask = get_object_or_404(Task, pk=supertask_pk)
    context = {
        'tasks': tasks,
        'breadcrumb': supertask.breadcrumb(),
        'base_template': 'crackers/base/_task.html',
    }
    return render(request, 'crackers/index.html', context)


def create(request, supertask_pk=None):
    if request.method == 'POST':
        form = TaskForm(data=request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            if supertask_pk is not None:
                task.supertask = get_object_or_404(Task, pk=supertask_pk)
                redirect_to = redirect('tracks:tasks', supertask_pk)
            else:
                redirect_to = redirect('tracks:index')
            task.save()
            return redirect_to
    else:
        form = TaskForm()
    context = {
        'form': form,
        'title': 'Create Objective',
    }
    if supertask_pk:
        context['action'] = reverse_lazy('tracks:create_subtask', kwargs={'supertask_pk': supertask_pk})
    else:
        context['action'] = reverse_lazy('tracks:create')
    return render(request, 'crackers/create.html', context)


def detail(request, supertask_pk):
    supertask = get_object_or_404(Task, pk=supertask_pk)
    context = {
        'supertask': supertask,
        'subtasks': supertask.subtasks.filter(supertask=supertask_pk),
    }
    trigger = {
        'change-offcanvas-title': {
            'title': supertask.title
        }
    }
    return render(request, 'crackers/components/detail.html', context, trigger=trigger)


# # create task (*task : subtask right under an objective)
# def create_task(request, objective_pk):   
#     if request.method == 'POST':
#         form = TaskForm(data=request.POST)
#         if form.is_valid():
#             task = form.save(commit=False)
#             task.objective = get_object_or_404(Objective, pk=objective_pk)
#             task.save()
#             return redirect('tracks:tasks', objective_pk)
#     else:
#         form = TaskForm()
#     context = {
#         'form': form,
#         'objective_pk': objective_pk,
#         'title': 'Create Task',
#         'action': reverse_lazy('tracks:create_task', kwargs={'objective_pk': objective_pk})
#     }
#     return render(request, 'crackers/create.html', context)


# def create_subtask(request, supertask_pk):
#     if request.method == 'POST':
#         form = TaskForm(data=request.POST)
#         if form.is_valid():
#             task = form.save(commit=False)
#             task.supertask = get_object_or_404(Task, pk=supertask_pk)
#             task.objective = task.supertask.objective
#             task.save()
#             return redirect('tracks:subtasks', supertask_pk)
#     else:
#         form = TaskForm()
#     context = {
#         'form': form,
#         'supertask_pk': supertask_pk,
#         'title': 'Create Task',
#         'action': reverse_lazy('tracks:create_subtask', kwargs={'supertask_pk': supertask_pk})
#     }
#     return render(request, 'crackers/create.html', context)




# def task_detail(request, supertask_pk):
#     context = {
#         'task': get_object_or_404(Task, pk=supertask_pk)
#     }
#     trigger = {
#         'change-offcanvas-title': {
#             'title': context['task'].title
#         }
#     }
#     return render(request, 'crackers/components/task_detail.html', context, trigger=trigger)


# def update(request, objective_pk):   # Objective Update
#     objective = get_object_or_404(Objective, pk=objective_pk)
#     if request.method == 'PUT':
#         data = QueryDict(request.body).dict()
#         form = ObjectiveForm(data=data, instance=objective)
#         if form.is_valid():
#             form.save()
#             return redirect(request.META.get('HTTP_REFERER'))
#     else:
#         form = ObjectiveForm(instance=objective)
#     context = {
#         'form': form,
#         'title': 'Update Objective',
#     }
#     return render(request, 'crackers/update.html', context)


# def update_task(request, task_pk):
#     task = get_object_or_404(Task, pk=task_pk)
#     if request.method == 'PUT':
#         data = QueryDict(request.body).dict()
#         form = TaskForm(data=data, instance=task)
#         if form.is_valid():
#             form.save()
#             if task.supertask is None:
#                 redirect_to = reverse_lazy('tracks:tasks', kwargs={'objective_pk': task.objective.pk})
#             else:
#                 redirect_to = reverse_lazy('tracks:subtasks', kwargs={'supertask_pk': task.supertask.pk})
#             return HTTPResponseHXRedirect(redirect_to=redirect_to)
#     else:
#         form = TaskForm(instance=task)
#     context = {
#         'form': form,
#         'title': 'Update Task',
#     }
#     return render(request, 'crackers/update.html', context)


# def delete(request, objective_pk):
#     objective = get_object_or_404(Objective, pk=objective_pk)
#     objective.delete()
#     # redirect시 trigger에 대한 코드 실행 후 페이지가 바뀐다. 어떻게 유지할까
#     return HTTPResponseHXRedirect(redirect_to=reverse_lazy('tracks:index'))


# def delete_task(request, task_pk):
#     task = get_object_or_404(Task, pk=task_pk)
#     supertask = task.supertask
#     if supertask is None:
#         redirect_to = reverse_lazy('tracks:tasks', kwargs={'objective_pk': task.objective.pk})
#     else:
#         redirect_to = reverse_lazy('tracks:subtasks', kwargs={'supertask_pk': supertask.pk})
#     task.delete()
#     return HTTPResponseHXRedirect(redirect_to=redirect_to)