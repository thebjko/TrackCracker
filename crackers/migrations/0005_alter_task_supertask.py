# Generated by Django 4.2.2 on 2023-06-23 06:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('crackers', '0004_task_supertask'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='supertask',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='subtasks', to='crackers.task', verbose_name='supertask'),
        ),
    ]
