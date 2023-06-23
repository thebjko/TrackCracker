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

# def redirect_to_tasks(request, pk):
#     '''
#     for hx-get to redirect
#     tr 태그에 링크를 걸 수 있어서 사용
#     '''
#     return HTTPResponseHXRedirect(redirect_to=reverse_lazy('tracks:tasks', kwargs={'pk': pk}))


def tasks(request, pk):
    tasks = Task.objects.filter(supertask=pk)   # pk만 넘겨줘야 하나 아니면 객체를 넘겨줘야 하나?
    context = {
        'tasks': tasks,
    }
    return render(request, 'crackers/components/tr.html', context)
