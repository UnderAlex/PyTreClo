
    function deleteTask(taskId) {
        if (confirm("Вы уверены, что хотите удалить эту задачу?")) {
            fetch(`/tasks/${taskId}/delete/`, {
                method: "POST",
                headers: {
                    "X-CSRFToken": "{{ csrf_token }}"
                },
            })
            .then(response => {
                if (response.ok) {
                    location.reload();
                } else {
                    alert("Ошибка при удалении задачи.");
                }
            });
        }
    }
