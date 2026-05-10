from datetime import datetime
from django.utils import timezone
from django.db import models
from django.contrib.auth.models import User



class CategoryManager(models.Manager):

    def get_queryset(self):
        return super().get_queryset().filter(is_deleted=False)


class Category(models.Model):
    description = models.TextField(max_length=100)
    name = models.CharField(max_length=50)
    is_deleted = models.BooleanField(default=False)
    deleted_at = models.DateTimeField(null=True, blank=True)

    objects = CategoryManager()

    all_objects = models.Manager()

    def __str__(self):
        return self.name

    def delete(self, *args, **kwargs):
        self.is_deleted = True
        self.deleted_at = timezone.now()
        self.save()

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

    title = models.CharField(max_length=50, unique_for_date="created_at")
    description = models.TextField(max_length=100)
    categories = models.ManyToManyField(Category, related_name="tasks")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="new")
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tasks')

    deadline = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

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

    title = models.CharField(max_length=50, unique_for_date="created_at")
    description = models.TextField(max_length=100)
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='subtasks')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="new")
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='subtasks')

    deadline = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

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
