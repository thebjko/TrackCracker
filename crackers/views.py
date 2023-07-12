from django.http import QueryDict
from django.shortcuts import render, redirect, get_object_or_404
from django.template import loader
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods, require_GET
from django.core.paginator import Paginator  
from django.db.models import Q

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
        data = request.POST
        path = data.get('_path')
        form = TaskForm(data=data)
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
        context['supertask'] = get_object_or_404(Task, pk=supertask_pk)
        context['action'] = reverse_lazy('tracks:create_subtask', kwargs={'supertask_pk': supertask_pk})
    else:
        context['action'] = reverse_lazy('tracks:create')
    return render(request, 'crackers/create.html', context)


@require_GET
def detail(request, supertask_pk):
    if request.user.is_authenticated:
        supertask = get_object_or_404(Task, pk=supertask_pk, user=request.user)
        paginator = Paginator(supertask.subtasks.order_by('pk'), 5)
        page = request.GET.get('page', '1')
        page_obj = paginator.get_page(page)
        context = {
            'supertask': supertask,
            'page_obj': page_obj,
            'subtasks': supertask.subtasks.filter(supertask=supertask_pk),
        }
        trigger = {
            'change-detail-btn': {
                'btnId': f'detail-btn-for-{supertask.pk}',
                'outerHTML': loader.render_to_string('crackers/components/detail_btn.html', {'supertask': supertask}, request)
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


@login_required
def detail_paginator(request, supertask_pk):
    page = request.GET.get('page', '1')
    supertask = get_object_or_404(Task, pk=supertask_pk, user=request.user)
    paginator = Paginator(supertask.subtasks.order_by('pk'), 5)
    page_obj = paginator.get_page(page)
    context = {
        'page_obj': page_obj,
        'supertask': supertask,
    }
    trigger = {
        'update-paginator': {
            'paginatorId': f'paginator-{supertask.pk}',
            'innerHTML': loader.render_to_string('crackers/components/paginator.html', context, request)
        }
    }
    return render(request, 'crackers/components/subtasks.html', context, trigger=trigger)


@login_required
def move_objective(request, task_pk):
    if request.method == 'POST':
        current_task = get_object_or_404(Task, pk=task_pk, user=request.user)
        current_supertask = current_task.supertask
        current_task.supertask = None
        current_task.save()
        if current_supertask:
            current_supertask.achievement = current_supertask.assess_achievement()
            current_supertask.save()
        return redirect('tracks:index')
    else:
        query = Q(supertask=None) & Q(user=request.user) & ~Q(pk=task_pk)
        tasks = Task.objects.filter(query).order_by('-pk')
        current_task = get_object_or_404(Task, pk=task_pk, user=request.user)
    context = {
        'tasks': tasks,
        'current_task': current_task,
        'target_pk': None,
    }
    return render(request, 'crackers/move.html', context)


def move_task(request, task_pk, target_pk):
    if request.method == 'POST':
        current_task = get_object_or_404(Task, pk=task_pk, user=request.user)
        target = get_object_or_404(Task, pk=target_pk, user=request.user)
        current_supertask = current_task.supertask
        current_task.supertask = target
        current_task.save()
        current_supertask.achievement = current_supertask.assess_achievement()
        current_supertask.save()
        return redirect('tracks:tasks', target_pk)
    else:
        query = Q(supertask=target_pk) & Q(user=request.user) & ~Q(pk=task_pk)
        tasks = Task.objects.filter(query).order_by('-pk')
        current_task = get_object_or_404(Task, pk=task_pk, user=request.user)
        supertask = get_object_or_404(Task, pk=target_pk, user=request.user)
    context = {
        'tasks': tasks,
        'current_task': current_task,
        'target_pk': target_pk,
        'breadcrumb': supertask.breadcrumb(),
    }
    return render(request, 'crackers/move.html', context)