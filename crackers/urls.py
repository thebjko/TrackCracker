from django.urls import path

from . import views

app_name = 'tracks'
urlpatterns = [
    path('', views.index, name='index'),
    path('<int:pk>/', views.tasks, name='tasks'),
    path('<int:pk>/redirect/', views.redirect_to_tasks, name='redirect_to_tasks'),
    path('create/', views.create, name='create'),
    path('<int:pk>/create/', views.create, name='create'),
]