from django.urls import path

from .views import (
    CategoryDetailUpdateDeleteView,
    CategoryListCreateAPIView,
    SubTaskDetailUpdateDeleteView,
    SubTaskListCreateAPIView,
    TaskListCreateAPIView,
    TaskRetrieveUpdateDestroyAPIView,
    task_by_weekday,
    task_statistics,
)

urlpatterns = [
    path("tasks/", TaskListCreateAPIView.as_view(), name="task-list-create"),
    path(
        "tasks/<int:id>/",
        TaskRetrieveUpdateDestroyAPIView.as_view(),
        name="task-detail",
    ),
    path("tasks/statistics/", task_statistics, name="task-statistics"),
    path("subtasks/", SubTaskListCreateAPIView.as_view(), name="subtask-list-create"),
    path(
        "subtasks/<int:id>/",
        SubTaskDetailUpdateDeleteView.as_view(),
        name="subtask-detail",
    ),
    path("tasks/by-day/", task_by_weekday, name="task-by-weekday"),
    path(
        "categories/", CategoryListCreateAPIView.as_view(), name="category-list-create"
    ),
    path(
        "categories/<int:id>/",
        CategoryDetailUpdateDeleteView.as_view(),
        name="category-detail",
    ),
]