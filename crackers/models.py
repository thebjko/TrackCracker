from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.db.models import F, FloatField, Sum


class Task(models.Model):
    title = models.CharField('title', max_length=100)
    description = models.TextField('description', null=True, blank=True)
    objective = models.ForeignKey('crackers.Objective', verbose_name='objective', on_delete=models.CASCADE, related_name='tasks')
    supertask = models.ForeignKey('self', verbose_name='supertask', on_delete=models.CASCADE, blank=True, null=True, related_name='subtasks')
    type = models.CharField('type', max_length=50, null=True, blank=True, default=None)
    completed = models.BooleanField('completed', default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    duration = models.DurationField('duration', null=True, blank=True)
    
    proportion = models.IntegerField('proportion', validators=[MinValueValidator(0)])   # 이 Task가 Supertask 또는 Objective에서 차지하는 비중
    total = models.IntegerField('total', default=10_000)
    achievement = models.FloatField('achievement', default=0, validators=[MaxValueValidator(1.0), MinValueValidator(0.0)])
    
    class Meta:
        db_table = 'task'

    # def save(self, *args, **kwargs):
    #     super().save(*args, **kwargs)
    #     print('save called')


class Objective(models.Model):
    title = models.CharField('title', max_length=100)
    description = models.TextField('description', null=True, blank=True)
    type = models.CharField('type', max_length=50, null=True, blank=True, default=None)
    completed = models.BooleanField('completed', default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    duration = models.DurationField('duration', null=True, blank=True)
    total = models.IntegerField('total', default=10_000)
    
    @property
    def achievement(self):
        weighted_achievement_total = self.tasks.annotate(
            weighted_achievement=F('achievement')*F('proportion')   # self를 사용하면 RecurssionError 발생
        ).aggregate(
            weighted_achievement_total=Sum('weighted_achievement', output_field=FloatField())
        ).get('weighted_achievement_total', 0)
        total = self.tasks.aggregate(total=Sum('proportion', output_field=FloatField())).get('total')
        return weighted_achievement_total / total
    
    class Meta:
        db_table = 'objective'
