from django.contrib import admin
from .models import Board, Task, Tag

admin.site.register(Board)
admin.site.register(Task)
admin.site.register(Tag)