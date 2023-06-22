from django.urls import path

from . import views

app_name = 'crackers'
urlpatterns = [
    path('', views.index, name='index'),
]