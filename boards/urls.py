from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('create-board/', views.create_board, name='create_board'),
    path('board/<int:board_id>/', views.board_detail, name='board_detail'),
    path('board/<int:board_id>/create-task/', views.create_task, name='create_task'),
    path('task/<int:task_id>/update/', views.update_task_status, name='update_task_status'),
				path('task/<int:task_id>/update-status/', views.update_task_status, name='update_task_status'),
				path('board/<int:board_id>/update-title/', views.update_board_title, name='update_board_title'),
    path('task/<int:task_id>/update/', views.update_task, name='update_task'),
				path('tasks/<int:task_id>/delete/', views.delete_task, name='delete_task'),
				path('board/<int:board_id>/delete/', views.delete_board, name='delete_board'),
				path("api/tasks/<int:board_id>/", views.get_tasks_for_board, name="get_tasks_for_board"),
				path('api/tasks/<int:board_id>/', views.get_tasks_by_board, name='api_tasks'),
    path('board/<int:board_id>/update/', views.update_board, name='update_board'),
]
