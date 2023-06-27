from django.db import models

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
    proportion = models.IntegerField('proportion')   # 이 Task가 Supertask 또는 Objective에서 차지하는 비중
    total = models.IntegerField('total', default=10_000)
    
    @property
    def achievement(self):
        pass

    class Meta:
        db_table = 'task'


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
        pass

    class Meta:
        db_table = 'objective'
