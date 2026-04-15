from django.db.models import Count, Q
from django.http import HttpResponse
from django.utils import timezone

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.generics import ListAPIView, CreateAPIView, RetrieveAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Task, Category, SubTask
from .serializers import TaskSerializer,SubTaskSerializer, SubTaskCreateSerializer


# OopCompanion:suppressRename


def index(request):
    return HttpResponse(
        "Hello, Serhii !!!."
    )


def page(request):
    return HttpResponse(
        "My first page !!!."
    )


class TaskCreateView(CreateAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer


class TaskListView(ListAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer


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


class SubTaskListCreateView(APIView):
    def get(self, request):
        subtasks = SubTask.objects.all()
        serializer = SubTaskSerializer(subtasks, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = SubTaskCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SubTaskDetailUpdateDeleteView(APIView):
    def get_object(self, pk):
        try:
            return SubTask.objects.get(pk=pk)
        except SubTask.DoesNotExist:
            return None

    def get(self, request, pk):
        subtask = self.get_object(pk)
        if not subtask:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = SubTaskSerializer(subtask)
        return Response(serializer.data)

    def put(self, request, pk):
        subtask = self.get_object(pk)
        if not subtask:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = SubTaskCreateSerializer(subtask, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        subtask = self.get_object(pk)
        if not subtask:
            return Response(status=status.HTTP_404_NOT_FOUND)
        subtask.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)