from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.db.models import F, FloatField, Sum, Case, When, Max, Subquery, OuterRef
from django.db.models.functions import Coalesce

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
    accumulative = models.BooleanField('accumulative', default=False)   # 서브태스크 생성시 proportion을 누적합으로 입력할 수 있게
    
    # if accumulative, where to start?
    start = models.IntegerField(default=0)
    
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
            subtasks = self.subtasks.order_by('proportion')
            reference = F('proportion')
            proportion_total = Sum('proportion', output_field=FloatField())
            if self.accumulative:
                subquery = Subquery(
                    self.subtasks.order_by('-proportion').filter(proportion__lte=OuterRef('proportion')).exclude(pk=OuterRef('pk')).annotate(last=Max('proportion', output_field=FloatField())).values('last')[:1]
                )
                subtasks = subtasks.annotate(last=subquery).annotate(adjusted_weight=F('proportion')-Coalesce('last', self.start, output_field=FloatField()))
                reference = F('adjusted_weight')
                proportion_total = Max('proportion', output_field=FloatField())
            weighted_achievement_total = subtasks.annotate(
                weighted_achievement=Case(   # pseudo_achievement
                    When(completed=True, then=reference),
                    default=F('achievement')*reference,
                    output_field=FloatField(),
                )
            ).values('weighted_achievement').aggregate(
                weighted_achievement_total=Sum('weighted_achievement', output_field=FloatField())
            ).get('weighted_achievement_total', 0)
            total = subtasks.aggregate(
                total=proportion_total
            ).get('total', 1)
            return weighted_achievement_total / total
        if self.completed:
            return 1.0
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
        supertask = self.supertask
        super().save(*args, **kwargs)
        achievement_reassessment_signal.send(sender=self.__class__, supertask=supertask)

    def delete(self, *args, **kwargs):
        supertask = self.supertask
        result = super().delete(*args, **kwargs)
        achievement_reassessment_signal.send(sender=self.__class__, supertask=supertask)
        return result

    class Meta:
        db_table = 'task'
