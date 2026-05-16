from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone

from .models import Task


@receiver(pre_save, sender=Task)
def track_task_status_change(sender, instance, **kwargs):
    if instance.pk:
        try:
            instance._previous_status = Task.objects.get(pk=instance.pk).status
        except Task.DoesNotExist:
            instance._previous_status = None
    else:
        instance._previous_status = None


@receiver(post_save, sender=Task)
def send_task_status_notification(sender, instance, created, **kwargs):
    if created:
        return
    
    if not instance.owner:
        return
    
    previous_status = getattr(instance, '_previous_status', None)
    
    if previous_status and previous_status != instance.status:
        send_status_change_email(instance, previous_status, instance.status)


def send_status_change_email(task, old_status, new_status):
    subject = f"Статус задачи изменен: {task.title}"
    message = f"""
Уважаемый {task.owner.first_name or task.owner.username}!

Статус вашей задачи был изменен.

Название задачи: {task.title}
Описание: {task.description}
Предыдущий статус: {old_status}
Новый статус: {new_status}
Дата изменения: {timezone.now().strftime('%Y-%m-%d %H:%M:%S')}

С уважением,
Система управления задачами
"""
    
    try:
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL if hasattr(settings, 'DEFAULT_FROM_EMAIL') else 'noreply@taskmanager.com',
            recipient_list=[task.owner.email],
            fail_silently=False,
        )
        print(f"Email notification sent to {task.owner.email} for task '{task.title}' status change: {old_status} -> {new_status}")
    except Exception as e:
        print(f"Failed to send email notification: {e}")
