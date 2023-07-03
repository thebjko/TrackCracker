from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.db.models import F, FloatField, Sum, Case, When

from .signals import achievement_reassessment_signal


class Task(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField('title', max_length=100)
    description = models.TextField('description', null=True, blank=True)
    supertask = models.ForeignKey('self', verbose_name='supertask', on_delete=models.CASCADE, blank=True, null=True, related_name='subtasks')
    completed = models.BooleanField('completed', default=False)
    # marked_complete = models.BooleanField('marked complete', default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    proportion = models.IntegerField('proportion', validators=[MinValueValidator(0)])   # 이 Task가 Supertask 또는 Objective에서 차지하는 비중
    achievement = models.FloatField('achievement', default=0, validators=[MaxValueValidator(1.0), MinValueValidator(0.0)])
    # accumulative = models.BooleanField('accumulative', default=False)   # 서브태스크 생성시 proportion을 누적합으로 입력할 수 있게
    
    # type = models.CharField('type', max_length=50, null=True, blank=True, default=None)
    # duration = models.DurationField('duration', null=True, blank=True)
    # total = models.IntegerField('total', default=10_000)


    @property
    def pseudo_achievement(self):
        if self.completed:
            return 1.0
        return self.achievement


    @property
    def marked_complete(self):
        return self.completed and self.subtasks.filter(completed=False, achievement__lt=1.0).exists()


    def assess_achievement(self):
        if self.subtasks.exists():
            weighed_achievement_total = self.subtasks.annotate(
                weighted_achievement=Case(   # use pseudo_achievement
                    When(completed=True, then=F('proportion')),
                    default=F('achievement')*F('proportion'),
                    output_field=FloatField(),
                )
            ).aggregate(
                weighed_achievement_total=Sum('weighted_achievement', output_field=FloatField())
            ).get('weighed_achievement_total', 0)
            total = self.subtasks.aggregate(
                total=Sum('proportion', output_field=FloatField())
            ).get('total', 1)
            return weighed_achievement_total / total
        else:
            return 0.0


    def breadcrumb(self):
        crumb = [self]
        supertask = self.supertask
        while supertask is not None:
            crumb.append(supertask)
            supertask = supertask.supertask
        # return reversed(crumb)   # iterator, not list
        crumb.reverse()
        return crumb
    

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        achievement_reassessment_signal.send(sender=self.__class__, supertask=self.supertask)


    def delete(self, *args, **kwargs):
        supertask = self.supertask
        result = super().delete(*args, **kwargs)
        achievement_reassessment_signal.send(sender=self.__class__, supertask=supertask)
        return result

    
    class Meta:
        db_table = 'task'
