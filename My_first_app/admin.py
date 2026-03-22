from django.contrib import admin
from django.contrib.admin import action

from My_first_app.models import Task, Category, SubTask


# Register your models here.
class InlineTaskAdmin(admin.StackedInline):
    model = SubTask




@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'description']
    search_fields = ['name']
    list_filter = ['name']
    list_per_page = 2

class SubTaskInline(admin.StackedInline):
    model = SubTask
    extra = 1
    max_num = 10
    readonly_fields = ['created_at']
    verbose_name = 'SubTask'
    verbose_name_plural = 'SubTasks'
    fieldsets = (

    )


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ['title', 'get_categories','status', 'deadline']
    search_fields = ['title']
    list_filter = ['status', 'categories']
    list_editable = ["status"]
    list_per_page = 10
    inlines = [SubTaskInline]

    def cut_title(self,obj):
        if len(obj.title) > 10:
            return obj.title[:10] + "..."
        else:
            return obj.title

    def get_categories(self, obj):
        return ", ".join([category.name for category in obj.categories.all()])
    get_categories.short_description = 'Categories'


@admin.register(SubTask)
class SubTaskAdmin(admin.ModelAdmin):
    list_display = ['title', 'task','status', 'deadline']
    search_fields = ['title']
    list_filter = ['task', 'status']
    list_editable = ["status"]
    list_per_page = 10


    actions = ["mark_done"]
    @admin.action(description='Mark selected subtasks as Done')
    def mark_done(self, request, queryset):
        queryset.update(status='done')
        self.message_user(request, "Selected subtasks marked as done")