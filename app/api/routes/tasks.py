from fastapi import APIRouter, Depends, HTTPException
from app.core.services.task_service import TaskService
from app.core.services.auth_service import get_current_user
from app.core.models.user import User
from app.adapters.repositories.base import SessionLocal
from pydantic import BaseModel

router = APIRouter(prefix="/tasks", tags=["tasks"])

@router.get("/")
def get_tasks(current_user: User = Depends(get_current_user)):
    db = SessionLocal()
    task_service = TaskService(db)
    return task_service.get_tasks(current_user.id)

class TaskCreate(BaseModel):
    title: str

@router.post("/")
def create_task(task: TaskCreate, current_user: User = Depends(get_current_user)):
    db = SessionLocal()
    task_service = TaskService(db)
    return task_service.create_task(current_user.id, task.title)


class TaskUpdate(BaseModel):
    completed: bool

@router.put("/{task_id}")
def update_task(task_id: int, task: TaskUpdate, current_user: User = Depends(get_current_user)):
    db = SessionLocal()
    task_service = TaskService(db)
    updated_task = task_service.update_task(task_id, current_user.id, completed=task.completed)
    if not updated_task:
        raise HTTPException(status_code=404, detail="Task not found")
    return updated_task

@router.delete("/{task_id}")
def delete_task(task_id: int, current_user: User = Depends(get_current_user)):
    db = SessionLocal()
    task_service = TaskService(db)
    task = task_service.delete_task(task_id, current_user.id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return {"message": "Task deleted"}