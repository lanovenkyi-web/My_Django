from rest_framework import serializers
from .models import Task, Category, SubTask
from datetime import datetime


# OopCompanion:suppressRename

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'status', 'deadline', 'created_at', 'categories']
        read_only_fields = ['id', 'created_at']
        extra_kwargs = {
            'categories': {'required': False}
        }


class SubTaskCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubTask
        fields = ['id', 'title', 'description', 'task', 'status', 'deadline', 'created_at']
        read_only_fields = ['id', 'created_at']





class CategoryCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'description']

    def create(self, validated_data):
        if Category.objects.filter(name=validated_data['name']).exists():
            raise serializers.ValidationError("Категория с таким названием уже существует")
        return super().create(validated_data)

    def update(self, instance, validated_data):
        if 'name' in validated_data and Category.objects.filter(name=validated_data['name']).exclude(
                id=instance.id).exists():
            raise serializers.ValidationError("Категория с таким названием уже существует")
        return super().update(instance, validated_data)


class SubTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubTask
        fields = ['id', 'title', 'description', 'status', 'deadline', 'created_at']


class TaskDetailSerializer(serializers.ModelSerializer):
    subtasks = SubTaskSerializer(many=True, read_only=True)

    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'status', 'deadline', 'created_at', 'categories', 'subtasks']
        read_only_fields = ['id', 'created_at']





class TaskCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'status', 'deadline', 'created_at', 'categories']
        read_only_fields = ['id', 'created_at']

    def validate_deadline(self, value):
        if value < datetime.now():
            raise serializers.ValidationError("Дата дедлайна не может быть в прошлом")
        return value