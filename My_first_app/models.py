
from django.utils import timezone
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator


# OopCompanion:suppressRename


class CustomUser(AbstractUser):
    email = models.EmailField(unique=True, verbose_name="Email")
    username = models.CharField(
        max_length=150,
        unique=True,
        validators=[
            RegexValidator(
                regex=r'^[a-zA-Z0-9_]+$',
                message='Username can only contain letters, numbers, and underscores'
            )
        ],
        verbose_name="Username"
    )
    first_name = models.CharField(max_length=30, blank=True, verbose_name="First Name")
    last_name = models.CharField(max_length=30, blank=True, verbose_name="Last Name")
    date_joined = models.DateTimeField(auto_now_add=True, verbose_name="Date Joined")
    is_active = models.BooleanField(default=True, verbose_name="Active")
    is_verified = models.BooleanField(default=False, verbose_name="Email Verified")
    
    groups = models.ManyToManyField(
        'auth.Group',
        verbose_name='groups',
        blank=True,
        help_text='The groups this user belongs to.',
        related_name="customuser_set",
        related_query_name="customuser",
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name='user permissions',
        blank=True,
        help_text='Specific permissions for this user.',
        related_name="customuser_set",
        related_query_name="customuser",
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    class Meta:
        db_table = 'my_first_app_customuser'
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def __str__(self):
        return self.email


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
    owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='tasks', null=True, blank=True)

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
    owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='subtasks', null=True, blank=True)

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
