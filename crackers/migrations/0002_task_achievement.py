# Generated by Django 4.2.2 on 2023-06-28 00:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crackers', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='achievement',
            field=models.FloatField(default=0, verbose_name='achievement'),
        ),
    ]