from django.urls import path

from . import views

app_name = 'tracks'
urlpatterns = [
    path('', views.index, name='index'),   # all objectives
    path('create/', views.create, name='create'),   # create objective

    path('objective/<int:pk>/', views.tasks, name='tasks'),   # tasks under objective of pk
    # path('objective/<int:pk>/create/', views.create_task, name='create_task'),    # create subtask under supertask
    # path('subtasks/<int:supertask_pk>/', views.subtasks, name='subtasks'),   # subtasks under supertask of pk
    # path('subtasks/<int:supertask_pk>/create/', views.create_task, name='create_task'),    # create subtask under supertask
    
    path('<int:pk>/redirect/', views.redirect_to_create, name='redirect_to_create'),
    path('<int:pk>/detail/', views.detail, name='detail'),
    path('update/', views.update, name='update'),
    path('<int:pk>/update/', views.update, name='update'),
    path('<int:pk>/delete/', views.delete, name='delete'),
]