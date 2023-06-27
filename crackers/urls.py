from django.urls import path

from . import views

app_name = 'tracks'
urlpatterns = [
    path('', views.index, name='index'),   # all objectives
    path('create/', views.create, name='create'),   # create objective
    path('objective/<int:objective_pk>/update/', views.update, name='update'),   # tasks under objective of pk
    path('objective/<int:objective_pk>/delete/', views.delete, name='delete'),

    path('objective/<int:objective_pk>/', views.tasks, name='tasks'),   # tasks under objective of pk
    path('objective/<int:objective_pk>/detail/', views.detail, name='detail'),
    path('objective/<int:objective_pk>/create/', views.create_task, name='create_task'),    # create subtask under supertask
    
    path('subtasks/<int:supertask_pk>/', views.subtasks, name='subtasks'),   # subtasks under supertask of pk
    path('subtasks/<int:supertask_pk>/detail/', views.task_detail, name='task_detail'),
    path('subtasks/<int:supertask_pk>/create/', views.create_subtask, name='create_subtask'),    # create subtask under supertask
]