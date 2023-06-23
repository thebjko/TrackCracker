from django.db import models

# Create your models here.
class Objective(models.Model):
    title = models.CharField('title', max_length=100)
    description = models.TextField('description')

    @property
    def achievement(self):
        pass


class Subtask(models.Model):
    objective = models.ForeignKey('crackers.Objective', verbose_name='objective', on_delete=models.CASCADE)
    task = models.ForeignKey('self', verbose_name='subtask', on_delete=models.CASCADE, blank=True, null=True)

    def save(self, **kwargs):
        self.task
        return super().save(**kwargs)
    
    @property
    def achievement(self):
        pass