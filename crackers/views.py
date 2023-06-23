from django.shortcuts import render, redirect

from .forms import ObjectiveForm
from .models import Objective


def index(request):
    objectives = Objective.objects.all()
    context = {
        'objectives': objectives,
    }
    return render(request, 'crackers/index.html', context)


def create(request):
    if request.method == 'POST':
        form  = ObjectiveForm(data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('tracks:index')
    else:
        form = ObjectiveForm()
    context = {
        'form': form,
    }
    return render(request, 'crackers/objectives/create.html', context)

