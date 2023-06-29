from django.http import QueryDict
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy, resolve
from django.db.models import F, FloatField, Sum

from .forms import TaskForm
from .models import Task
from .utils import render, HttpResponse, HTTPResponseHXRedirect

def index(request):
    tasks = Task.objects.filter(supertask=None)
    context = {
        'tasks': tasks,
        'base_template': 'crackers/base/_objective.html',
    }
    return render(request, 'crackers/tasks.html', context)


def tasks(request, supertask_pk):
    tasks = Task.objects.filter(supertask=supertask_pk)   # pk만 넘겨도 된다.
    supertask = get_object_or_404(Task, pk=supertask_pk)
    context = {
        'tasks': tasks,
        'supertask': supertask,
        'breadcrumb': supertask.breadcrumb(),
        'base_template': 'crackers/base/_task.html',
    }
    return render(request, 'crackers/tasks.html', context)


def create(request, supertask_pk=None):
    if request.method == 'POST':
        path = request.POST.get('_path')
        form = TaskForm(data=request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            if supertask_pk is not None:
                task.supertask = get_object_or_404(Task, pk=supertask_pk)
            task.save()
            return redirect(path)
    else:
        form = TaskForm()
        path = request.META.get('HTTP_REFERER')
    context = {
        'form': form,
        'title': 'Create Objective',
        'path': path,
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


def delete(request, task_pk):
    task = get_object_or_404(Task, pk=task_pk)
    task.delete()
    return redirect(request.META.get('HTTP_REFERER'))
    # redirect시 trigger에 대한 코드 실행 후 페이지가 바뀐다. 어떻게 유지할까
    # return HTTPResponseHXRedirect(redirect_to=reverse_lazy('tracks:index'))


def update(request, task_pk):
    task = get_object_or_404(Task, pk=task_pk)
    if request.method == 'PUT':
        data = QueryDict(request.body).dict()
        path = data.pop('_path')
        form = TaskForm(data=data, instance=task)
        if form.is_valid():
            form.save()
            # detail에서 수정했을때는 supertask로 가야한다.
            # return HTTPResponseHXRedirect(redirect_to=reverse_lazy('tracks:tasks', kwargs={'supertask_pk': task_pk}))
            return HTTPResponseHXRedirect(redirect_to=path)
    else:
        form = TaskForm(instance=task)
        path = request.META.get('HTTP_REFERER')
    context = {
        'form': form,
        'path': path,
    }
    return render(request, 'crackers/update.html', context)


def complete(request, task_pk):
    task = get_object_or_404(Task, pk=task_pk)
    if task.completed:
        task.completed = False
        # subtasks로 현재 achievement 측정
        if task.subtasks.exists():
            weighed_achievement_total = task.subtasks.annotate(
                weighted_achievement=F('achievement')*F('proportion')
            ).aggregate(
                weighed_achievement_total=Sum('weighted_achievement', output_field=FloatField())
            ).get('weighed_achievement_total', 0)
            total = task.subtasks.aggregate(
                total=Sum('proportion', output_field=FloatField())
            ).get('total', 1)
            task.achievement = weighed_achievement_total / total
        else:
            task.achievement = 0.0
        task.save()
    else:
        task.completed = True
        task.achievement = 1.0
        task.save()
    trigger = {
        'change-achievement-width': {
            'identifier': f'task-progress-{task.pk}',
            'width': round(task.achievement*100, 1),
        },
    }
    return HttpResponse(trigger=trigger)