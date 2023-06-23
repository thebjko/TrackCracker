from django.shortcuts import render

from .models import Objective


def index(request):
    objectives = Objective.objects.all()
    context = {
        'objectives': objectives,
    }
    return render(request, 'crackers/index.html', context)