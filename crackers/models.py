from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from .signals import achievement_reassessment_signal

class Task(models.Model):
    title = models.CharField('title', max_length=100)
    description = models.TextField('description', null=True, blank=True)
    supertask = models.ForeignKey('self', verbose_name='supertask', on_delete=models.CASCADE, blank=True, null=True, related_name='subtasks')
    completed = models.BooleanField('completed', default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    proportion = models.IntegerField('proportion', validators=[MinValueValidator(0)])   # 이 Task가 Supertask 또는 Objective에서 차지하는 비중
    achievement = models.FloatField('achievement', default=0, validators=[MaxValueValidator(1.0), MinValueValidator(0.0)])
    
    # type = models.CharField('type', max_length=50, null=True, blank=True, default=None)
    # duration = models.DurationField('duration', null=True, blank=True)
    # total = models.IntegerField('total', default=10_000)
    
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
