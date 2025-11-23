from typing import List

from fastapi import Depends, APIRouter
from sqlalchemy.orm import Session
from src.core.database import get_session
from src.tasks import service
from src.tasks.schemas import TaskCreate, TaskRead, TaskUpdate

router = APIRouter(prefix="/tasks", tags=["tasks"])

@router.get("/{task_id}", response_model=TaskRead)
def get_task(task_id: int, session: Session = Depends(get_session)) -> TaskRead:
    return service.get_task_by_id(task_id, session)

@router.get("/", response_model=List[TaskRead])
def get_tasks(session: Session = Depends(get_session)) -> List[TaskRead]:
    return service.get_tasks(session)

@router.post("/", response_model=TaskRead)
def create_task(task: TaskCreate, session: Session = Depends(get_session)) -> TaskRead:
    return service.create_new_task(task, session)

@router.put("/{task_id}", response_model=TaskRead)
def update_task(task_id: int, task_update: TaskUpdate, session: Session = Depends(get_session)) -> TaskRead:
    return service.update_task(task_id, task_update, session)

@router.delete("/{task_id}", status_code=204)
def delete_task(task_id: int, session: Session = Depends(get_session)):
    return service.delete_task(task_id, session)