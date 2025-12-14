from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class TaskBase(BaseModel):
    workflow_id: int
    name: str
    description: Optional[str] = None
    order: int
    model_configuration: Optional[str] = None

class TaskCreate(TaskBase):
    pass

class TaskUpdate(TaskBase):
    pass

class TaskInDBBase(TaskBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        from_attributes = True

class Task(TaskInDBBase):
    pass

class TaskInDB(TaskInDBBase):
    pass