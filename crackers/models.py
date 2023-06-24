from django.db import models

class Task(models.Model):
    title = models.CharField('title', max_length=100)
    description = models.TextField('description', null=True, blank=True)
    supertask = models.ForeignKey('self', verbose_name='supertask', on_delete=models.CASCADE, blank=True, null=True, related_name='subtasks')
    type = models.CharField('type', max_length=50, null=True, blank=True, default=None)
    completed = models.BooleanField('completed', default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    duration = models.DurationField('duration', null=True, blank=True)
    
    @property
    def achievement(self):
        pass

    class Meta:
        db_table = 'task'


# class Subtask(models.Model):
#     objective = models.ForeignKey('crackers.Objective', verbose_name='objective', on_delete=models.CASCADE)
#     task = models.ForeignKey('self', verbose_name='subtask', on_delete=models.CASCADE, blank=True, null=True)

#     def save(self, *args, **kwargs):
#         super().save(*args, **kwargs)
#         if self.task is None:
#             self.task = self
#             super().save(*args, **kwargs)
    
#     @property
#     def achievement(self):
#         pass

#     class Meta:
#         db_table = 'subtasks'