import json
from django.http import JsonResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, redirect, get_object_or_404
from .models import Board, Task, Tag
from datetime import date, datetime

def home(request):
    """
    Главная страница: отображает список всех бордов.
    """
    boards = Board.objects.all()
    return render(request, 'boards/home.html', {'boards': boards})

def create_board(request):
    """
    Создание нового борда.
    - Проверяет на наличие дубликата по названию.
    - Ограничение на максимум 6 бордов.
    """
    if request.method == "POST":
        title = request.POST.get("title")

        # Проверка на уникальность названия борда
        if Board.objects.filter(title=title).exists():
            return render(request, 'boards/home.html', {
                'error': 'Board with this title already exists!',
                'boards': Board.objects.all()
            })

        # Проверка на количество бордов
        if Board.objects.count() >= 6:
            return render(request, 'boards/home.html', {
                'error': 'You can only create up to 6 boards!',
                'boards': Board.objects.all()
            })

        # Создание нового борда
        Board.objects.create(title=title)
        return redirect('home')

    return redirect('home')

def board_detail(request, board_id):
    board = get_object_or_404(Board, id=board_id)
    tasks_todo = board.tasks.filter(status='todo')
    tasks_in_progress = board.tasks.filter(status='in_progress')
    tasks_done = board.tasks.filter(status='done')
    tags = Tag.objects.all()  # Получение всех тегов

    return render(request, 'boards/board_detail.html', {
        'board': board,
        'tasks_todo': tasks_todo,
        'tasks_in_progress': tasks_in_progress,
        'tasks_done': tasks_done,
        'tags': tags,  # Передача тегов в контекст
    })

def create_task(request, board_id):
    board = get_object_or_404(Board, id=board_id)

    if request.method == "POST":
        title = request.POST.get("title")
        description = request.POST.get("description")
        expired_date = request.POST.get("expired_date")  # Получаем дату как строку
        status = request.POST.get("status")
        tag_id = request.POST.get("tag")  # Получаем id тега из формы

        tag = Tag.objects.filter(id=tag_id).first() if tag_id else None

        try:
            expired_date_obj = datetime.strptime(expired_date, "%Y-%m-%d").date()  # Преобразуем строку в дату
            if expired_date_obj < date.today():
                raise ValueError("Expired date cannot be in the past!")
        except ValueError as e:
            return render(request, 'boards/board_detail.html', {
                'board': board,
                'error': str(e),
            })

        if board.tasks.count() >= 10:
            return render(request, 'boards/board_detail.html', {
                'board': board,
                'error': 'You can only create up to 10 tasks per board!',
            })

        if Task.objects.filter(title=title).exists():
            return render(request, 'boards/board_detail.html', {
                'board': board,
                'error': 'Task with this title already exists!',
            })

        # Создаём задачу
        Task.objects.create(
            title=title,
            description=description,
            expired_date=expired_date,
            status=status,
            board=board,
            tag=tag,
        )
        return redirect('board_detail', board_id=board.id)

    # Передача всех тегов в контекст для отображения в форме
    tags = Tag.objects.all()
    return render(request, 'boards/board_detail.html', {'board': board, 'tags': tags})

@csrf_exempt
def update_task_status(request, task_id):
    if request.method == "POST":
        try:
            # Попробуем сначала обработать JSON-запрос
            try:
                data = json.loads(request.body)
                status = data.get('status')
            except json.JSONDecodeError:
                # Если JSON не удалось декодировать, используем POST-данные
                status = request.POST.get('status')

            # Проверка валидности статуса
            if status not in ['todo', 'in_progress', 'done']:
                return JsonResponse({'error': 'Invalid status'}, status=400)

            # Обновление задачи
            task = get_object_or_404(Task, id=task_id)
            task.status = status
            task.save()

            # Если запрос пришёл через AJAX, возвращаем JSON
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({'message': 'Status updated successfully', 'task_id': task.id})

            # Если это обычный POST-запрос, перенаправляем на страницу
            return redirect('board_detail', board_id=task.board.id)

        except Task.DoesNotExist:
            return JsonResponse({'error': 'Task not found'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)

@csrf_exempt
def update_board_title(request, board_id):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            new_title = data.get("title")

            if not new_title:
                return JsonResponse({"success": False, "error": "Название не может быть пустым"})

            board = get_object_or_404(Board, id=board_id)
            board.title = new_title
            board.save()

            return JsonResponse({"success": True})
        except Exception as e:
            return JsonResponse({"success": False, "error": str(e)})

    return JsonResponse({"success": False, "error": "Неверный метод запроса"})

def update_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)

    if request.method == "POST":
        title = request.POST.get("title")
        description = request.POST.get("description")
        expired_date = request.POST.get("expired_date")  # Получаем дату как строку
        status = request.POST.get("status")
        tag_id = request.POST.get("tag")

        # Проверяем валидность данных
        if not title or not expired_date or status not in ['todo', 'in_progress', 'done']:
            return HttpResponseBadRequest("Неверные данные")

        try:
            expired_date_obj = datetime.strptime(expired_date, "%Y-%m-%d").date()  # Преобразуем строку в дату
        except ValueError:
            return HttpResponseBadRequest("Неверный формат даты")

        tag = Tag.objects.filter(id=tag_id).first() if tag_id else None

        # Обновляем задачу
        task.title = title
        task.description = description
        task.expired_date = expired_date_obj
        task.status = status
        task.tag = tag
        task.save()

        return redirect('board_detail', board_id=task.board.id)

    return HttpResponseBadRequest("Неверный метод запроса")

@csrf_exempt
def delete_task(request, task_id):
    if request.method == "POST":
        task = get_object_or_404(Task, id=task_id)
        board_id = task.board.id
        task.delete()
        return JsonResponse({"success": True, "board_id": board_id})
    return JsonResponse({"success": False, "error": "Неверный метод запроса"})


@csrf_exempt
def delete_board(request, board_id):
    board = get_object_or_404(Board, id=board_id)
    if not board.tasks.exists():
        board.delete()
        return redirect('home')
    return JsonResponse({"success": False, "error": "Cannot delete a project with tasks."})


def get_tasks_for_board(request, board_id):
    board = get_object_or_404(Board, id=board_id)
    tasks = board.tasks.values("title", "expired_date")
    return JsonResponse({"tasks": list(tasks)})

def get_tasks_by_board(request, board_id):
    tasks = Task.objects.filter(board_id=board_id).values('id', 'title', 'expired_date')
    return JsonResponse({'tasks': list(tasks)})

def update_board(request, board_id):
    if request.method == "POST":
        board = get_object_or_404(Board, id=board_id)
        title = request.POST.get("title")
        color = request.POST.get("color")

        if title:
            board.title = title
        if color:
            board.color = color

        board.save()
        return JsonResponse({"success": True, "title": board.title, "color": board.color})
    return JsonResponse({"success": False, "error": "Invalid request method"}, status=400)
