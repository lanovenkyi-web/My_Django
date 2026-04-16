from django.urls import path
from .views import SubTaskListCreateView, SubTaskDetailUpdateDeleteView
from . import views

urlpatterns = [
    path('tasks/create/', views.TaskCreateView.as_view(), name='task-create'),
    path('tasks/', views.TaskListView.as_view(), name='task-list'),
    path('tasks/<int:pk>/', views.TaskDetailView.as_view(), name='task-detail'),
    path('tasks/statistics/', views.task_statistics, name='task-statistics'),
    path('subtasks/', SubTaskListCreateView.as_view(), name='subtask-list-create'),
    path('subtasks/<int:pk>/', SubTaskDetailUpdateDeleteView.as_view(), name='subtask-detail-update-delete'),
    path('tasks/by-day/', views.task_by_weekday, name='task-by-weekday'),

]
