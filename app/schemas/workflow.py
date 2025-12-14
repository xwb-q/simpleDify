from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime
import json

class TaskBase(BaseModel):
    name: str
    description: Optional[str] = None
    type: str = "llm"
    config: Optional[str] = None
    order: int = 0

class TaskCreate(TaskBase):
    pass

class TaskUpdate(TaskBase):
    pass

class Task(TaskBase):
    id: int
    workflow_id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

class WorkflowBase(BaseModel):
    name: str
    description: Optional[str] = None

class WorkflowCreate(WorkflowBase):
    pass

class WorkflowUpdate(WorkflowBase):
    pass

class Workflow(WorkflowBase):
    id: int
    created_at: datetime
    updated_at: datetime
    tasks: List[Task] = []
    
    class Config:
        from_attributes = True
