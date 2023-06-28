from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.db.models import Sum, FloatField


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
    
    proportion = models.FloatField('proportion', validators=[MaxValueValidator(1.0), MinValueValidator(0.0)])   # 이 Task가 Supertask 또는 Objective에서 차지하는 비중
    total = models.IntegerField('total', default=10_000)
    achievement = models.FloatField('achievement', default=0)
    
    class Meta:
        db_table = 'task'

    # def save(self, *args, **kwargs):
    #     super().save(*args, **kwargs)
    #     if self.supertask:
    #         self.supertask.subtasks.aggregate(models.Sum(''))


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
        total = self.tasks.aggregate(total=Sum('proportion', output_field=FloatField())).get('total')
        completed = self.tasks.filter(completed=True).aggregate(comp=Sum('proportion', output_field=FloatField())).get('comp')
        return completed / total * 100

    class Meta:
        db_table = 'objective'
