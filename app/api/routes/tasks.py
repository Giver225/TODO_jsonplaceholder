from fastapi import APIRouter
from app.core.services.task_service import TaskService

router = APIRouter(prefix="/tasks", tags=["tasks"])
task_service = TaskService()

@router.get("/")
def get_tasks():
    return task_service.get_tasks()

@router.post("/")
def create_task(task_data: dict):
    return task_service.create_task(task_data)

@router.put("/{task_id}")
def update_task(task_id: int, task_data: dict):
    return task_service.update_task(task_id, task_data)