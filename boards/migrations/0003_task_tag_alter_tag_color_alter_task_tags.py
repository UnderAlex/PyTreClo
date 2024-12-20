# Generated by Django 5.1.4 on 2024-12-20 02:55

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('boards', '0002_task_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='tag',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='single_tag_tasks', to='boards.tag'),
        ),
        migrations.AlterField(
            model_name='tag',
            name='color',
            field=models.CharField(default='#000000', max_length=7),
        ),
        migrations.AlterField(
            model_name='task',
            name='tags',
            field=models.ManyToManyField(blank=True, related_name='multi_tag_tasks', to='boards.tag'),
        ),
    ]