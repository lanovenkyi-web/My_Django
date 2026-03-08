from datetime import datetime

from django.db import models


# Create your models here.
class Category(models.Model):
    description: str = models.TextField(max_length=100, verbose_name="Категория выполнения")
    name: str = models.CharField(max_length=50, verbose_name="Название категории")

    def __str__(self):
        return self.name


class Task(models.Model):
    STATUS_CHOICES = [
        ("new", "New"),
        ("in_progress", "In progress"),
        ("pending", "Pending"),
        ("blocked", "Blocked"),
        ("done", "Done"),
    ]
    title: str = models.CharField(max_length=50, unique_for_date="created_at", verbose_name="Название задачи")

    description: str = models.TextField(max_length=100, verbose_name="Описание задачи")

    categories: str = models.ManyToManyField(Category, related_name="tasks", verbose_name="Категории задачи")

    status: str = models.CharField(max_length=20, choices=STATUS_CHOICES, default="new", verbose_name="Статус задачи")

    deadline: datetime = models.DateTimeField(help_text="Дата и время дедлайн")

    created_at: datetime = models.DateTimeField(auto_now_add=True, help_text="Дата и время создания")

    def __str__(self):
        return self.title


class SubTask(models.Model):
    STATUS_CHOICES = [
        ("new", "New"),
        ("in_progress", "In progress"),
        ("pending", "Pending"),
        ("blocked", "Blocked"),
        ("done", "Done"),
    ]
    title: str = models.CharField(max_length=50, unique_for_date="created_at", verbose_name="Название подзадачи")
    description: str = models.TextField(max_length=100, verbose_name="Описание подзадачи")
    task: str = models.ForeignKey(Task, on_delete=models.CASCADE,
related_name='subtasks', help_text='Основная задача')
    status: str = models.CharField(max_length=20, choices=STATUS_CHOICES, default="new", verbose_name="Статус задачи")
    deadline: datetime = models.DateTimeField(help_text="Дата и время дедлайн")
    created_at: datetime = models.DateTimeField(auto_now_add=True, help_text="Дата и время создания")

    def __str__(self):
        return self.title