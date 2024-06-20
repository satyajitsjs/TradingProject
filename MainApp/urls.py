from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('result/<task_id>/', views.result, name='result'),
    path('task-status/<task_id>/', views.task_status, name='task_status'),
]
