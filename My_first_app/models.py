from datetime import datetime
from django.db import models


# OopCompanion:suppressRename



class Category(models.Model):

    description = models.TextField(max_length=100, verbose_name="Категория выполнения")
    name = models.CharField(max_length=50, verbose_name="Название категории")

    def __str__(self):
        return self.name

    class Meta:
        db_table = "task_manager_category"
        verbose_name = "Category"
        verbose_name_plural = "Categories"
        constraints = [
            models.UniqueConstraint(
                fields=['name'],
                name='unique_category'
            )
        ]


class Task(models.Model):
    STATUS_CHOICES = [
        ("new", "New"),
        ("in_progress", "In progress"),
        ("pending", "Pending"),
        ("blocked", "Blocked"),
        ("done", "Done"),
    ]

    title = models.CharField(max_length=50, unique_for_date="created_at", verbose_name="Название задачи")
    description = models.TextField(max_length=100, verbose_name="Описание задачи")
    categories = models.ManyToManyField(Category, related_name="tasks", verbose_name="Категории задачи")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="new", verbose_name="Статус задачи")


    deadline = models.DateTimeField(help_text="Дата и время дедлайна", null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, help_text="Дата и время создания")

    def __str__(self):
        return self.title

    class Meta:
        db_table = "task_manager_task"
        verbose_name = "Task"
        verbose_name_plural = "Tasks"
        constraints = [
            models.UniqueConstraint(
                fields=['title'],
                name='unique_task'
            )
        ]
        ordering = ["-created_at"]


class SubTask(models.Model):
    STATUS_CHOICES = [
        ("new", "New"),
        ("in_progress", "In progress"),
        ("pending", "Pending"),
        ("blocked", "Blocked"),
        ("done", "Done"),
    ]

    title = models.CharField(max_length=50, unique_for_date="created_at", verbose_name="Название подзадачи")
    description = models.TextField(max_length=100, verbose_name="Описание подзадачи")
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='subtasks', help_text='Основная задача')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="new", verbose_name="Статус задачи")


    deadline = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, help_text="Дата и время создания")

    def __str__(self):
        return self.title

    class Meta:
        db_table = "task_manager_subtask"
        verbose_name = "Subtask"
        verbose_name_plural = "Subtasks"
        constraints = [
            models.UniqueConstraint(
                fields=['title'],
                name='unique_subtask'
            )
        ]
        ordering = ["-created_at"]