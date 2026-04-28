from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Count, Q
from django.http import HttpResponse
from django.utils import timezone

from rest_framework import status, filters
from rest_framework.decorators import api_view
from rest_framework.generics import ListAPIView, CreateAPIView, RetrieveAPIView, GenericAPIView, \
    RetrieveUpdateDestroyAPIView, ListCreateAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Task, Category, SubTask
from .serializers import TaskSerializer, SubTaskSerializer, SubTaskCreateSerializer, TaskCreateSerializer, \
    TaskDetailSerializer


# OopCompanion:suppressRename


def index(request):
    return HttpResponse(
        "Hello, Serhii !!!."
    )


def page(request):
    return HttpResponse(
        "My first page !!!."
    )


class SubTaskPagination(PageNumberPagination):
    page_size = 5


# class TaskCreateView(CreateAPIView):
#    queryset = Task.objects.all()
#    serializer_class = TaskSerializer


class TaskListCreateAPIView(ListCreateAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskCreateSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]

    filterset_fields = ['status', 'deadline']
    search_fields = ['title', 'description']
    ordering_fields = ['created_at']
    ordering = ['-created_at']

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return TaskCreateSerializer
        return TaskSerializer

class TaskRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Task.objects.all()
    #serializer_class = TaskSerializer
    lookup_field = 'id'

    def get_serializer_class(self):
        if self.request.method in ['PUT','PATCH']:
            return TaskCreateSerializer
        return TaskDetailSerializer


class TaskDetailView(RetrieveAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer


@api_view(['GET'])
def task_statistics(request):
    total_tasks = Task.objects.count()

    status_counts = Task.objects.values('status').annotate(count=Count('id'))

    overdue_tasks = Task.objects.filter(
        deadline__lt=timezone.now(),
        status__in=['new', 'in_progress', 'pending', 'blocked']
    ).count()

    statistics = {
        'total_tasks': total_tasks,
        'tasks_by_status': list(status_counts),
        'overdue_tasks': overdue_tasks,
    }

    return Response(statistics)


class SubTaskListCreateAPIView(ListCreateAPIView):
    queryset = SubTask.objects.all()
    serializer_class = SubTaskSerializer
    pagination_class = SubTaskPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status', 'deadline']
    search_fields = ['title', 'description']
    ordering_fields = ['created_at']
    ordering = ['-created_at']


class SubTaskDetailUpdateDeleteView(RetrieveUpdateDestroyAPIView):
    queryset = SubTask.objects.all()
    lookup_field = 'id'

    def get_serializer_class(self):
        if self.request.method in ['PUT','PATCH']:
            return SubTaskCreateSerializer
        return SubTaskSerializer

@api_view(['GET'])
def task_by_weekday(request):
    weekday_map = {
        'monday': 2, 'tuesday': 3, 'wednesday': 4, 'thursday': 5,
        'friday': 6, 'saturday': 7, 'sunday': 1
    }
    tasks = Task.objects.all()
    weekday_param = request.query_params.get('day_of_week')

    if weekday_param:
        weekday_number = weekday_map.get(weekday_param.lower())
        if weekday_number:
            tasks = tasks.filter(created_at__week_day=weekday_number)

    serializer = TaskSerializer(tasks, many=True)
    return Response(serializer.data)