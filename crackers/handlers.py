from django.db.models import F, FloatField, Sum
from django.dispatch import receiver

from .models import Task
from .signals import achievement_reassessment_signal


@receiver(achievement_reassessment_signal, sender=Task)
def reassess_achievement(sender, **kwargs):
    supertask = kwargs.get('supertask')
    if supertask is not None and supertask.completed == False:
        if supertask.subtasks.exists():
            # 최상위 Task가 아닌 경우. 완료 표시가 된 경우 1.0으로 유지
            weighted_achievement_total = supertask.subtasks.annotate(
                weighted_achievement=F('achievement')*F('proportion')
            ).aggregate(
                weighted_achievement_total=Sum('weighted_achievement', output_field=FloatField())
            ).get('weighted_achievement_total', 0)
            total = supertask.subtasks.aggregate(
                total=Sum('proportion', output_field=FloatField())
            ).get('total', 1)
            supertask.achievement = weighted_achievement_total / total
            if supertask.achievement == 1.0:
                supertask.completed = True
            else:
                supertask.completed = False
            supertask.save()   # 여기서 호출된 save 메서드 또한 post_save 신호를 발생시킨다.
        else:
            supertask.achievement = 0.0
            supertask.save()
