from django.dispatch import receiver

from .models import Task
from .signals import achievement_reassessment_signal


@receiver(achievement_reassessment_signal, sender=Task)
def reassess_achievement(sender, **kwargs):
    supertask = kwargs.get('supertask')
    if supertask is not None:
        supertask.achievement = supertask.assess_achievement()
        # 여기서 호출된 save 메서드 또한 post_save 신호를 발생시킨다.
        if supertask.achievement == 1.0:
            supertask.completed = True
        else:
            supertask.completed = False
        supertask.save()
