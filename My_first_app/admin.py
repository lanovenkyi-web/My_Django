from django.contrib import admin

from My_first_app.models import *


# admin.site.register(Task)
# admin.site.register(SubTask)
# admin.site.register(Category)


class SubTaskInline(admin.TabularInline):
    model = SubTask


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = [
        "title",
        "status",
        "deadline"
    ]
    search_fields = ["title"]
    list_filter = [
        "status",
        "categories",
    ]
    list_editable = [
        "status"
    ]
    list_per_page = 10


@admin.register(SubTask)
class SubTaskAdmin(admin.ModelAdmin):
    list_display = [
        "title",
        "task",
        "status",
        "deadline"
    ]
    search_fields = ["title"]
    list_filter = [
        "status",
        "task",
    ]
    list_editable = [
        "status"
    ]
    list_per_page = 10


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = [
        "name"
    ]
    search_fields = ["name"]
    list_per_page = 10
