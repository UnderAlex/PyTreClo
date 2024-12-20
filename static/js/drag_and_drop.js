document.addEventListener('DOMContentLoaded', () => {
    const todoList = document.getElementById('todo');
    const inProgressList = document.getElementById('in_progress');
    const doneList = document.getElementById('done');

    [todoList, inProgressList, doneList].forEach(list => {
        new Sortable(list, {
            group: 'tasks',
            animation: 150,
            onEnd: async (event) => {
                const taskId = event.item.dataset.taskId;
                const newStatus = event.to.id;

                if (!taskId || !newStatus) {
                    alert('Ошибка: не удалось определить ID задачи или статус.');
                    return;
                }

                // Отправка данных на сервер
                const response = await fetch(`/task/${taskId}/update-status/`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': '{{ csrf_token }}',
                    },
                    body: JSON.stringify({ status: newStatus }),
                });

                if (!response.ok) {
                    alert('Ошибка при обновлении статуса задачи.');
                    console.error(await response.json());
                }
            }
        });
    });
});
