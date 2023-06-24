from django.urls import path

from . import views

app_name = 'tracks'
urlpatterns = [
    path('', views.index, name='index'),
    path('<int:pk>/', views.tasks, name='tasks'),
    path('create/', views.create, name='create'),
    path('<int:pk>/create/', views.create, name='create'),
    path('<int:pk>/redirect/', views.redirect_to_create, name='redirect_to_create'),
    path('<int:pk>/detail/', views.detail, name='detail'),
]