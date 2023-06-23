from django.urls import path

from . import views

app_name = 'tracks'
urlpatterns = [
    path('', views.index, name='index'),
    path('create/', views.create, name='create'),
    path('<int:pk>/tasks/', views.tasks, name='tasks'),
    # path('<int:pk>/redirect_to_tasks/', views.redirect_to_tasks, name='redirect_to_tasks'),
]