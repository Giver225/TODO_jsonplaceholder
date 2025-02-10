// Общие функции для обеих страниц
let token = localStorage.getItem("token");

// Функция для отображения сообщений об ошибках (можно заменить на модальное окно)
function showError(message) {
    alert(message);
}

// Функция для отображения сообщений об успехе (можно заменить на модальное окно)
function showSuccess(message) {
    alert(message);
}


// Логика для страницы авторизации
if (window.location.pathname === "/") {
    document.getElementById("loginForm").addEventListener("submit", async (e) => {
        e.preventDefault();
        const username = document.getElementById("loginUsername").value;
        const password = document.getElementById("loginPassword").value;
    
        const response = await fetch("/api.php", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({ action: "login", username, password }),
        });
    
        try {
            const result = await response.json();
    
            if (response.ok) {  // Проверяем HTTP-статус
                if (result.access_token) {
                    localStorage.setItem("token", result.access_token);
                    window.location.href = "/tasks";
                } else {
                    alert("Login failed: " + (result.detail || "Unknown error"));
                }
            }
            else {
                // Обрабатываем ошибку
                
                if (result.error == "HTTP error: 401 - {\"detail\":\"Incorrect username or password\"}") {
                    alert("Incorrect username or password. Please try again.");
                } else {
                    alert("Login failed: " + (result.error || "Unknown error"));
                }
            }
        } catch (error) {
            console.error("Error:", error);
            alert("An error occurred during login.");
        }
    });

    document.getElementById("registerForm").addEventListener("submit", async (e) => {
        e.preventDefault();
        const username = document.getElementById("registerUsername").value;
        const password = document.getElementById("registerPassword").value;
    
        const response = await fetch("/api.php", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({ action: "register", username, password }),
        });
    
        try {
            const result = await response.json();
    
            if (response.ok) {
                console.log(result);
                
                if (result.message === "User registered successfully") {
                    alert("User registered successfully");
                } else {
                    alert("Registration failed: " + (result.detail || "Unknown error"));
                }
            } else {
                // Обрабатываем ошибку
                if (result.error && result.error == 'HTTP error: 400 - {"detail":"Username already registered"}') {
                    alert("This username is already taken. Please choose a different one.");
                } else {
                    alert("Registration failed: " + (result.error || "Unknown error"));
                }
            }
        } catch (error) {
            console.error("Registration error:", error);
            alert("An error occurred during registration.");
        }
    });
    
}


// Логика для страницы задач
if (window.location.pathname === "/tasks") {
    // Проверка токена перед загрузкой контента
    const token = localStorage.getItem("token");

    if (!token) {
        window.location.href = "/";  // Перенаправляем на страницу авторизации
    } else {
        fetch("/api.php", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({ action: "check_token", token }),
        })
        .then(response => {
            if (response.status === 401) {  // Unauthorized
                localStorage.removeItem("token");
                window.location.href = "/";
            } else {
                // Если токен валиден, отображаем контент
                document.body.classList.remove("hidden");
                return response.json();
            }
        })

    }

    // Функция для загрузки задач
function loadTasks(tasks) {
    const taskList = document.getElementById("taskList");
    taskList.innerHTML = "";  // Очищаем список задач

    tasks.forEach(task => {
        const li = document.createElement("li");
        li.textContent = `${task.title} - ${task.completed ? "Completed" : "Not Completed"}`;

        const completeButton = document.createElement("button");
        completeButton.textContent = "Toggle Complete";
        completeButton.onclick = () => toggleComplete(task.id, !task.completed);

        const deleteButton = document.createElement("button");
        deleteButton.textContent = "Delete";
        deleteButton.onclick = () => deleteTask(task.id);

        li.appendChild(completeButton);
        li.appendChild(deleteButton);
        taskList.appendChild(li);
    });
}



    // Обработчик для кнопки выхода
    document.getElementById("logoutButton").addEventListener("click", () => {
        localStorage.removeItem("token");  // Удаляем токен
        window.location.href = "/";  // Перенаправляем на страницу авторизации
    });

    // Загружаем задачи при загрузке страницы
    fetch("/api.php", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({ action: "get_tasks", token: localStorage.getItem("token") }),
    })
    .then(response => {
        if (response.status === 401) {  // Unauthorized
            localStorage.removeItem("token");
            window.location.href = "/";
        } else {
            return response.json();
        }
    })
    .then(data => {
        if (data) {
            loadTasks(data);  // Загружаем задачи
        }
    })
    .catch(error => {
        console.error("Error:", error);
    });

    // Обработчик для формы создания задачи
    document.getElementById("createTaskForm").addEventListener("submit", async (e) => {
        e.preventDefault();  // Предотвращаем стандартное поведение формы

        const title = document.getElementById("taskTitle").value;
        const token = localStorage.getItem("token");

        if (!title) {
            alert("Please enter a task title");
            return;
        }

        try {
            const response = await fetch("/api.php", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({ action: "create_task", title, token }),
            });

            if (response.status === 401) {  // Unauthorized
                localStorage.removeItem("token");
                window.location.href = "/";
                return;
            }

            const result = await response.json();
            if (result.id) {
                // Перезагружаем список задач после успешного создания
                fetch("/api.php", {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json",
                    },
                    body: JSON.stringify({ action: "get_tasks", token }),
                })
                .then(response => response.json())
                .then(data => {
                    if (data) {
                        loadTasks(data);  // Загружаем обновлённый список задач
                    }
                });
            } else {
                alert("Failed to create task");
            }
        } catch (error) {
            console.error("Error:", error);
            alert("An error occurred while creating the task");
        }
    });
}

// Функция для переключения статуса задачи
async function toggleComplete(taskId, completed) {
    const response = await fetch("/api.php", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({ action: "update_task", task_id: taskId, completed, token: localStorage.getItem("token") }),
    });
    const result = await response.json();
    if (result.id) {
        // Перезагружаем список задач после успешного обновления
        fetch("/api.php", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({ action: "get_tasks", token: localStorage.getItem("token") }),
        })
        .then(response => response.json())
        .then(data => {
            if (data) {
                loadTasks(data);  // Загружаем обновлённый список задач
            }
        });
    } else {
        alert("Failed to update task");
    }
}

// Функция для удаления задачи
async function deleteTask(taskId) {
    const response = await fetch("/api.php", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({ action: "delete_task", task_id: taskId, token: localStorage.getItem("token") }),
    });
    const result = await response.json();
    if (result.message === "Task deleted") {
        // Перезагружаем список задач после успешного удаления
        fetch("/api.php", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({ action: "get_tasks", token: localStorage.getItem("token") }),
        })
        .then(response => response.json())
        .then(data => {
            if (data) {
                loadTasks(data);  // Загружаем обновлённый список задач
            }
        });
    } else {
        alert("Failed to delete task");
    }
}