from django.http import QueryDict
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods, require_GET, require_POST

from .forms import TaskForm
from .models import Task
from .utils import render, HttpResponse, HTTPResponseHXRedirect


@require_GET
def index(request):
    if request.user.is_authenticated:
        tasks = Task.objects.filter(supertask=None, user=request.user)
        context = {
            'tasks': tasks,
            'base_template': 'crackers/base/_objective.html',
        }
        return render(request, 'crackers/tasks.html', context)
    return render(request, 'crackers/landingpage.html')


@require_GET
@login_required
def tasks(request, supertask_pk):
    tasks = Task.objects.filter(supertask=supertask_pk, user=request.user)   # pk만 넘겨도 된다.
    supertask = get_object_or_404(Task, pk=supertask_pk, user=request.user)
    context = {
        'tasks': tasks,
        'supertask': supertask,
        'breadcrumb': supertask.breadcrumb(),
        'base_template': 'crackers/base/_task.html',
    }
    return render(request, 'crackers/tasks.html', context)


@require_http_methods(['GET', 'POST'])
@login_required
def create(request, supertask_pk=None):
    if request.method == 'POST':
        path = request.POST.get('_path')
        form = TaskForm(data=request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            if supertask_pk is not None:
                task.supertask = get_object_or_404(Task, pk=supertask_pk)
            task.user = request.user
            task.save()
            return redirect(path)
    else:
        form = TaskForm()
        path = request.META.get('HTTP_REFERER')
    context = {
        'form': form,
        'title': 'Create Objective' if supertask_pk is None else 'Create Task',
        'path': path,
    }
    if supertask_pk:
        context['action'] = reverse_lazy('tracks:create_subtask', kwargs={'supertask_pk': supertask_pk})
    else:
        context['action'] = reverse_lazy('tracks:create')
    return render(request, 'crackers/create.html', context)


@require_GET
def detail(request, supertask_pk):
    if request.user.is_authenticated:
        supertask = get_object_or_404(Task, pk=supertask_pk, user=request.user)
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
    return HTTPResponseHXRedirect(redirect_to=reverse_lazy('accounts:login'))


@require_http_methods(['DELETE'])
@login_required
def delete(request, task_pk):
    task = get_object_or_404(Task, pk=task_pk, user=request.user)
    supertask = task.supertask
    task.delete()
    if supertask is not None:
        # return redirect('tracks:tasks', supertask.pk)
        return HTTPResponseHXRedirect(redirect_to=reverse_lazy('tracks:tasks', kwargs={'supertask_pk': supertask.pk}))
    # return redirect('tracks:index')
    # redirect시 trigger에 대한 코드 실행 후 페이지가 바뀐다. 어떻게 유지할까
    return HTTPResponseHXRedirect(redirect_to=reverse_lazy('tracks:index'))


@require_http_methods(['GET', 'PUT'])
@login_required
def update(request, task_pk):
    task = get_object_or_404(Task, pk=task_pk, user=request.user)
    if request.method == 'PUT':
        data = QueryDict(request.body).dict()
        path = data.pop('_path')
        form = TaskForm(data=data, instance=task)
        if form.is_valid():
            form.save()
            return HTTPResponseHXRedirect(redirect_to=path)
    else:
        form = TaskForm(instance=task)
        path = request.META.get('HTTP_REFERER')
    context = {
        'form': form,
        'path': path,
    }
    return render(request, 'crackers/update.html', context)


@require_http_methods(['PUT'])
@login_required
def complete(request, task_pk):
    task = get_object_or_404(Task, pk=task_pk, user=request.user)
    if task.completed:
        if task.subtasks.exists() and not task.subtasks.filter(completed=False).exists():
            return HTTPResponseHXRedirect(redirect_to=request.META.get('HTTP_REFERER'))
        task.completed = False
        # task.supertask.completed = False
    else:
        task.completed = True
    task.achievement = task.assess_achievement()
    task.save()
    if task.marked_complete:
        trigger = {
            'task-marked-complete': {
                'identifier': f'task-progress-{task.pk}',
            },
        }
    else:
        trigger = {
            'change-achievement-width': {
                'identifier': f'task-progress-{task.pk}',
                'width': round(task.pseudo_achievement*100),
            },
        }
    if (supertask := task.supertask) is not None:
        if supertask.marked_complete:
            trigger['supertask-marked-complete'] = {
                'identifier': f'task-progress-{supertask.pk}',
            }
        else:
            trigger['change-supertask-achievement-width'] = {
                'identifier': f'task-progress-{supertask.pk}',
                'width': round(supertask.pseudo_achievement*100),
            }
    return HttpResponse(trigger=trigger)