// Общие функции для обеих страниц
let token = localStorage.getItem("token");

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
        const result = await response.json();
        if (result.access_token) {
            localStorage.setItem("token", result.access_token);
            window.location.href = "/tasks";
        } else {
            alert("Login failed: " + (result.detail || "Unknown error"));
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
        const result = await response.json();
        if (result.message === "User registered successfully") {
            alert("User registered successfully");
        } else {
            alert("Registration failed: " + (result.detail || "Unknown error"));
        }
    });
}

// Логика для страницы задач
if (window.location.pathname === "/tasks") {
    if (!token) {
        window.location.href = "/";
    } else {
        fetch("/api.php", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({ action: "check_token", token }),
        })
        .then(response => response.json())
        .then(data => {
            if (data.message !== "Token is valid") {
                window.location.href = "/";
            } else {
                loadTasks();
            }
        })
        .catch(() => {
            window.location.href = "/";
        });
    }

    document.getElementById("createTaskForm").addEventListener("submit", async (e) => {
        e.preventDefault();
        const title = document.getElementById("taskTitle").value;
        const response = await fetch("/api.php", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({ action: "create_task", title, token }),
        });
        const result = await response.json();
        if (result.id) {
            loadTasks();
        } else {
            alert("Failed to create task");
        }
    });

    document.getElementById("logoutButton").addEventListener("click", () => {
        localStorage.removeItem("token");
        window.location.href = "/";
    });

    async function loadTasks() {
        const response = await fetch("/api.php", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({ action: "get_tasks", token }),
        });
        const tasks = await response.json();
        const taskList = document.getElementById("taskList");
        taskList.innerHTML = "";
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

    async function toggleComplete(taskId, completed) {
        const response = await fetch("/api.php", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({ action: "update_task", task_id: taskId, completed, token }),
        });
        const result = await response.json();
        if (result.id) {
            loadTasks();
        } else {
            alert("Failed to update task");
        }
    }

    async function deleteTask(taskId) {
        const response = await fetch("/api.php", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({ action: "delete_task", task_id: taskId, token }),
        });
        const result = await response.json();
        if (result.message === "Task deleted") {
            loadTasks();
        } else {
            alert("Failed to delete task");
        }
    }
}