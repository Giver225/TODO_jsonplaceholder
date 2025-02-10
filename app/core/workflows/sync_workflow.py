from datetime import timedelta
from temporalio import workflow, activity
from temporalio.common import RetryPolicy
from app.adapters.clients.jsonplaceholder_client import JSONPlaceholderClient
from app.core.services.task_service import TaskService
from sqlalchemy.orm import Session
from app.adapters.repositories.base import SessionLocal
from app.adapters.cache.redis_cache import RedisCache

from hashlib import sha256

@activity.defn
async def sync_external_tasks_activity():
    client = JSONPlaceholderClient()
    service = TaskService(SessionLocal())
    cache = RedisCache()
    
    external_tasks = client.get_tasks()
    
    for ext_task in external_tasks:
        # Генерируем уникальный хеш задачи
        task_hash = sha256(
            f"{ext_task['userId']}-{ext_task['title']}-{ext_task['completed']}".encode()
        ).hexdigest()
        
        # Проверяем, есть ли хеш в кэше
        if not cache.get(f"task_hash:{task_hash}"):
            # Создаем задачу в БД
            service.create_task(
                user_id=ext_task["userId"],
                title=ext_task["title"],
                completed=ext_task["completed"]
            )
            # Сохраняем хеш в Redis на 7 дней
            cache.set(f"task_hash:{task_hash}", "1", ex=604800)
            

@activity.defn
async def clean_old_hashes_activity():
    cache = RedisCache()
    for key in cache.scan_iter("task_hash:*"):
        if cache.ttl(key) < 0:
            cache.delete(key)