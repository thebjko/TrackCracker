from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Task


@receiver(post_save, sender=Task)
def reassess_achievement(sender, task, **kwargs):
    print('post save handler')
    task.supertask.subtasks
