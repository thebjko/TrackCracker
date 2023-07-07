from django.urls import path

from . import views

app_name = 'tracks'
urlpatterns = [
    path('', views.index, name='index'),   # all objectives. 이후 로그인 되어있지 않으면 landingpage, 되어있다면 all objectives.
    path('create/', views.create, name='create'),   # create task
    path('<int:supertask_pk>/', views.tasks, name='tasks'),   # subtask list
    path('<int:supertask_pk>/create/', views.create, name='create_subtask'),   # create subtask
    path('<int:supertask_pk>/detail/', views.detail, name='detail'),
    path('<int:task_pk>/update/', views.update, name='update'),
    path('<int:task_pk>/delete/', views.delete, name='delete'),
    path('<int:task_pk>/complete/', views.complete, name='complete'),
    path('<int:supertask_pk>/detail_paginator/', views.detail_paginator, name='detail_paginator'),
]