from django.db import models

# Create your models here.
class Objective(models.Model):
    title = models.CharField('title', max_length=100)
    description = models.TextField('description')

    @property
    def achievement(self):
        pass

    class Meta:
        db_table = 'objectives'


class Subtask(models.Model):
    objective = models.ForeignKey('crackers.Objective', verbose_name='objective', on_delete=models.CASCADE)
    task = models.ForeignKey('self', verbose_name='subtask', on_delete=models.CASCADE, blank=True, null=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.task is None:
            self.task = self
            super().save(*args, **kwargs)
    
    @property
    def achievement(self):
        pass

    class Meta:
        db_table = 'subtasks'