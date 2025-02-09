from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.adapters.clients.jsonplaceholder_client import JSONPlaceholderClient
from app.core.models.task import Task
from app.core.models.user import User
from app.adapters.repositories.base import SessionLocal
import logging

logger = logging.getLogger(__name__)

def populate_database():
    
    """
    Получает данные из JSONPlaceholder API и вставляет их в PostgreSQL.
    """
    db = SessionLocal()
    print(f"populate_database is on")
    try:
        client = JSONPlaceholderClient()
        todos = client.get_tasks()  # Получаем данные из API

        for todo in todos:
            # Проверяем, существует ли пользователь с user_id
            # user = db.query(User).filter(User.id == todo["userId"]).first()
            # if not user:
            #     logger.info(f"User with id {todo['userId']} not found. Skipping task.")
            #     continue

            # Создаем объект Task на основе данных из API
            
            task = Task(
                id=todo["id"],
                title=todo["title"],
                completed=todo["completed"],
                user_id=todo["user_id"],
            )

            # Пытаемся добавить задачу в базу данных, если такая задача уже есть, ничего не делаем
            existing_task = db.query(Task).filter(Task.id == task.id).first()
            if not existing_task:
                db.add(task)

        db.commit()
        print("Database populated successfully!")
    except Exception as e:
        db.rollback()
        print(f"Error populating database: {e}")
    finally:
        db.close()
