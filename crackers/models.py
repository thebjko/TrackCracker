from django.db import models

# Create your models here.
class Task(models.Model):
    title = models.CharField('title', max_length=100)
    description = models.TextField('description')
    supertask = models.ForeignKey('self', verbose_name='supertask', on_delete=models.CASCADE, blank=True, null=True, related_name='subtasks')
    
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