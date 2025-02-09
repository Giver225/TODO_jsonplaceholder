import json
from datetime import timedelta
from sqlalchemy.orm import Session
from app.core.models.task import Task
from app.adapters.repositories.base import SessionLocal
from app.adapters.clients.jsonplaceholder_client import JSONPlaceholderClient
from app.adapters.cache.redis_cache import RedisCache
from sqlalchemy import func

class TaskService:
    def __init__(self, db: Session):
        self.db = db
        self.jsonplaceholder_client = JSONPlaceholderClient()
        self.cache = RedisCache()
        self.cache_ttl = timedelta(hours=1).seconds  # 1 час

    def get_tasks(self, user_id: int):
        cache_key = f"user:{user_id}:tasks"
        try:
            # Пытаемся получить данные из кэша
            cached_data = self.cache.get(cache_key)
            if cached_data:
                return json.loads(cached_data)
            
            # Если нет в кэше - запрос к БД
            with SessionLocal() as db:
                tasks = db.query(Task).filter(Task.user_id == user_id).all()
                serialized_tasks = [task.as_dict() for task in tasks]
                
                # Сохраняем в кэш
                self.cache.set(cache_key, json.dumps(serialized_tasks), ex=self.cache_ttl)
                return serialized_tasks
                
        except Exception as e:
            # Логирование ошибки кэша, но продолжаем работу
            return self._get_tasks_from_db(user_id)

    def create_task(self, user_id: int, title: str):
        try:
            with SessionLocal() as db:
                max_id = self.db.query(func.max(Task.id)).scalar()
                new_id = (max_id or 0) + 1
                task = Task(id = new_id, title=title, user_id=user_id)
                db.add(task)
                db.commit()
                db.refresh(task)

                # Инвалидация кэша
                self._invalidate_user_cache(user_id)
                
                return task.as_dict()
        except Exception as e:
            db.rollback()
            raise
        finally:
            db.close()

    def update_task(self, task_id: int, user_id: int, 
                   title: str = None, completed: bool = None):
        try:
            with SessionLocal() as db:
                task = db.query(Task).filter(
                    Task.id == task_id,
                    Task.user_id == user_id
                ).first()

                if not task:
                    return None

                if title: task.title = title
                if completed is not None: task.completed = completed
                
                db.commit()
                db.refresh(task)

                # Инвалидация кэша
                self._invalidate_user_cache(user_id)
                
                return task.as_dict()
        except Exception as e:
            db.rollback()
            raise
        finally:
            db.close()

    def delete_task(self, task_id: int, user_id: int):
        try:
            with SessionLocal() as db:
                task = db.query(Task).filter(
                    Task.id == task_id,
                    Task.user_id == user_id
                ).first()

                if not task:
                    return None

                db.delete(task)
                db.commit()

                # Инвалидация кэша
                self._invalidate_user_cache(user_id)
                
                return task.as_dict()
        except Exception as e:
            db.rollback()
            raise
        finally:
            db.close()

    def _get_tasks_from_db(self, user_id: int):
        """Фоллбек-метод для получения задач напрямую из БД"""
        with SessionLocal() as db:
            tasks = db.query(Task).filter(Task.user_id == user_id).all()
            return [task.as_dict() for task in tasks]

    def _invalidate_user_cache(self, user_id: int):
        """Инвалидация всех кэшированных данных пользователя"""
        cache_keys = [
            f"user:{user_id}:tasks",
            # Можно добавить другие ключи, связанные с пользователем
        ]
        for key in cache_keys:
            try:
                self.cache.client.delete(key)
            except Exception as e:
                # Логируем ошибку, но не прерываем выполнение
                pass