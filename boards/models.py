from django.db import models
from django.contrib.auth.models import User

class Tag(models.Model):
    name = models.CharField(max_length=20)
    color = models.CharField(max_length=7, default="#000000")  # HEX-код цвета

    def __str__(self):
        return self.name

class Board(models.Model):
    title = models.CharField(max_length=50, unique=True)
    color = models.CharField(max_length=7, default="#f8f9fa")  # HEX-код цвета (светло-серый по умолчанию)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Task(models.Model):
    STATUS_CHOICES = [
        ('todo', 'Сделать'),
        ('in_progress', 'В работе'),
        ('done', 'Готово'),
    ]
    title = models.CharField(max_length=20, unique=True)
    description = models.TextField(max_length=2000)
    created_at = models.DateTimeField(auto_now_add=True)
    expired_date = models.DateField()
    board = models.ForeignKey(Board, related_name='tasks', on_delete=models.CASCADE)
    assigned_user = models.ForeignKey(User, related_name='tasks', on_delete=models.SET_NULL, null=True)
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='todo')  # Поле статуса
    tag = models.ForeignKey(Tag, null=True, blank=True, on_delete=models.SET_NULL, related_name='single_tag_tasks')  # Уникальное related_name
    tags = models.ManyToManyField(Tag, blank=True, related_name='multi_tag_tasks')  # Уникальное related_name

    def __str__(self):
        return self.title
