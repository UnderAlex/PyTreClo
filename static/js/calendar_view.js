document.addEventListener("DOMContentLoaded", function () {
    const boardId = "{{ board.id }}"; // Правильная интерполяция ID доски
    const viewModeSelect = document.getElementById("viewModeSelect");
    const taskListView = document.getElementById("taskListView");
    const calendarView = document.getElementById("calendarView");
    const calendarBody = document.getElementById("calendarBody");

    function generateCalendar(tasks) {
        const now = new Date();
        const year = now.getFullYear();
        const month = now.getMonth();

        const firstDay = new Date(year, month, 1).getDay();
        const lastDate = new Date(year, month + 1, 0).getDate();

        calendarBody.innerHTML = "";

        const startOffset = firstDay === 0 ? 6 : firstDay - 1;

        let date = 1;
        for (let i = 0; i < 6; i++) {
            const row = document.createElement("tr");

            for (let j = 0; j < 7; j++) {
                const cell = document.createElement("td");

                if (i === 0 && j < startOffset) {
                    row.appendChild(cell);
                } else if (date > lastDate) {
                    row.appendChild(cell);
                } else {
                    cell.innerHTML = `<strong>${date}</strong>`;
                    cell.classList.add("calendar-date");

                    const dayTasks = tasks.filter(task => {
                        const taskDate = new Date(task.expired_date);
                        return (
                            taskDate.getFullYear() === year &&
                            taskDate.getMonth() === month &&
                            taskDate.getDate() === date
                        );
                    });

                    dayTasks.slice(0, 5).forEach(task => {
                        const taskDiv = document.createElement("div");
                        taskDiv.textContent = task.title;
                        taskDiv.classList.add("calendar-task");
                        cell.appendChild(taskDiv);
                    });

                    row.appendChild(cell);
                    date++;
                }
            }

            calendarBody.appendChild(row);
        }
    }

    fetch(`/api/tasks/${boardId}`) // Используем значение boardId
        .then(response => response.json())
        .then(data => {
            generateCalendar(data.tasks);
        })
        .catch(error => console.error("Ошибка загрузки задач:", error));

    viewModeSelect.addEventListener("change", function () {
        if (this.value === "calendarView") {
            taskListView.classList.add("d-none");
            calendarView.classList.remove("d-none");
        } else {
            taskListView.classList.remove("d-none");
            calendarView.classList.add("d-none");
        }
    });
});
