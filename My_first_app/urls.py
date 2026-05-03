from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (
    CategoryDetailUpdateDeleteView,
    CategoryListCreateAPIView,
    CategoryViewSet,
    SubTaskDetailUpdateDeleteView,
    SubTaskListCreateAPIView,
    TaskListCreateAPIView,
    TaskRetrieveUpdateDestroyAPIView,
    task_by_weekday,
    task_statistics,
)


router = DefaultRouter()
router.register(r'categories', CategoryViewSet, basename='category')

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

    path("", include(router.urls)),
    

    path(
        "categories-old/", CategoryListCreateAPIView.as_view(), name="category-list-create-old"
    ),
    path(
        "categories-old/<int:id>/",
        CategoryDetailUpdateDeleteView.as_view(),
        name="category-detail-old",
    ),
]