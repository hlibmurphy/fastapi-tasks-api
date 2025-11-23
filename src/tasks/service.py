from typing import List

from fastapi import HTTPException
from sqlalchemy.orm import Session
from src.tasks.model import Task
from src.tasks.schemas import TaskRead, TaskCreate


def get_tasks(session: Session) -> List[TaskRead]:
    tasks = session.query(Task).all()
    return [TaskRead.model_validate(task) for task in tasks]

def get_task_by_id(task_id: int, session: Session) -> TaskRead:
    task = session.get(Task, task_id)
    if task is None:
        raise HTTPException(status_code=404, detail=f"Task with id {task_id} not found")
    return TaskRead.model_validate(task)

def create_new_task(task_create: TaskCreate, session: Session) -> TaskRead:
    task = Task(**task_create.model_dump())
    session.add(task)
    session.commit()
    session.refresh(task)
    return TaskRead.model_validate(task)


