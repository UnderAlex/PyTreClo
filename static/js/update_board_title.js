document.addEventListener("DOMContentLoaded", function () {
    const titleElement = document.getElementById("board-title");

    // Отправка данных на сервер при нажатии Enter
    titleElement.addEventListener("keydown", function (event) {
        if (event.key === "Enter") {
            event.preventDefault(); // Останавливаем добавление новой строки
            titleElement.blur(); // Принудительно вызываем blur для сохранения изменений
        }
    });

    // Отправка данных на сервер при потере фокуса
    titleElement.addEventListener("blur", function () {
        const newTitle = titleElement.textContent.trim();
        const boardId = titleElement.getAttribute("data-board-id");

        // Проверка: отправлять только если текст изменился
        if (newTitle && newTitle !== titleElement.dataset.originalTitle) {
            fetch(`/board/${boardId}/update-title/`, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    "X-CSRFToken": "{{ csrf_token }}",
                },
                body: JSON.stringify({ title: newTitle }),
            })
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        console.log("Название доски обновлено");
                        titleElement.dataset.originalTitle = newTitle; // Обновляем сохранённое значение
                    } else {
                        alert("Ошибка обновления названия: " + data.error);
                    }
                })
                .catch(error => {
                    console.error("Ошибка:", error);
                });
        }
    });

    // Сохранение начального значения
    titleElement.dataset.originalTitle = titleElement.textContent.trim();
});
