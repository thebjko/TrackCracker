from django.db.models import F, FloatField, Sum
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from .models import Task


@receiver([post_save, post_delete], sender=Task)
def reassess_achievement(sender, instance, **kwargs):
    # 어떻게 테스트 할 것인가?
    # print('post save handler on', instance.pk)
    if instance.supertask is not None:
        weighted_achievement_total = instance.supertask.subtasks.annotate(
            weighted_achievement=F('achievement')*F('proportion')
        ).aggregate(
            weighted_achievement_total=Sum('weighted_achievement', output_field=FloatField())
        ).get('weighted_achievement_total', 0)
        total = instance.supertask.subtasks.aggregate(total=Sum('proportion', output_field=FloatField())).get('total')
        instance.supertask.achievement = weighted_achievement_total / total
        instance.supertask.save()   # 여기서 호출된 save 메서드는 post_save 신호를 발생시키는가?