import datetime
import os
import django
from datetime import timedelta
from django.utils import timezone


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "My_Django.settings")
django.setup()

from My_first_app.models import Category,Task, SubTask

Task.objects.filter(title="Prepare presentation").delete()

task = Task.objects.create(
title="Prepare presentation",

description="Prepare materials and slides for the presentation",

status="new",

deadline=timezone.now()+ timedelta(days=3),
)


subtask1 = SubTask.objects.create(
    title="Gather information",
    description="Find necessary information for the presentation",
    status="new",
    deadline=timezone.now()+ timedelta(days=2),

)


subtask2 = SubTask.objects.create(
    title="Create slides",
    description="Create presentation slides",
    status="new",
    deadline=timezone.now()+ timedelta(days=1),

)
#2==================================================================================

new_tasks = Task.objects.filter(status="new")

print(list(new_tasks))


expired_subtasks = SubTask.objects.filter(status="done",dedline__lt=timezone.now())
print(list(expired_subtasks))


#3==================================================================================

print("Update")

task_update = Task.objects.get(
title="Prepare presentation"
)
task_update.status = "in_progress"
task_update.save()
print(task_update)




subtask1_update = SubTask.objects.get(
    title="Gather information"
)
subtask1_update.deadline = timezone.now()- timedelta(days=2)
subtask1_update.save()
print(subtask1_update)




subtask2_update = SubTask.objects.get(
    title="Create slides"
)
subtask2_update.description = "Create and format presentation slides"
subtask2_update.save()
print(subtask2_update)


#4================================================================================
print("Delete")
task_dell=Task.objects.get(
    title="Prepare presentation"
)
print(task_dell)
task_dell.delete()
