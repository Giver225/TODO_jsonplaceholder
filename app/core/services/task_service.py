import requests
from app.core.models.task import Task
from app.adapters.repositories.base import SessionLocal

class TaskService:
    def __init__(self, db= SessionLocal):
        self.db = db
        self.jsonplaceholder_url = "https://jsonplaceholder.typicode.com/todos"

    def get_tasks(self, user_id: int):
        # Получаем задачи из PostgreSQL
        tasks = self.db.query(Task).filter(Task.user_id == user_id).all()
        return tasks

    def create_task(self, user_id: int, title: str):
        # Создаем задачу в PostgreSQL
        task = Task(title=title, user_id=user_id)
        self.db.add(task)
        self.db.commit()
        self.db.refresh(task)

        # Создаем задачу в JSONPlaceholder
        response = requests.post(self.jsonplaceholder_url, json={
            "title": title,
            "completed": False,
            "userId": user_id,
        })
        if response.status_code != 201:
            raise Exception("Failed to create task in JSONPlaceholder")

        return task

    def update_task(self, task_id: int, user_id: int, title: str = None, completed: bool = None):
        # Обновляем задачу в PostgreSQL
        task = self.db.query(Task).filter(Task.id == task_id, Task.user_id == user_id).first()
        if not task:
            return None
        if title:
            task.title = title
        if completed is not None:
            task.completed = completed
        self.db.commit()
        self.db.refresh(task)

        # Обновляем задачу в JSONPlaceholder
        response = requests.put(f"{self.jsonplaceholder_url}/{task_id}", json={
            "title": task.title,
            "completed": task.completed,
            "userId": user_id,
        })
        if response.status_code != 200:
            raise Exception("Failed to update task in JSONPlaceholder")

        return task

    def delete_task(self, task_id: int, user_id: int):
        # Удаляем задачу в PostgreSQL
        task = self.db.query(Task).filter(Task.id == task_id, Task.user_id == user_id).first()
        if not task:
            return None
        self.db.delete(task)
        self.db.commit()

        # Удаляем задачу в JSONPlaceholder
        response = requests.delete(f"{self.jsonplaceholder_url}/{task_id}")
        if response.status_code != 200:
            raise Exception("Failed to delete task in JSONPlaceholder")

        return task