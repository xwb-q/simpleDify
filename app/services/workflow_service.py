from sqlalchemy.orm import Session
from app.crud import workflow_crud
from app.schemas.workflow import WorkflowCreate, WorkflowUpdate

def get_workflow(db: Session, workflow_id: int):
    return workflow_crud.get_workflow(db, workflow_id)

def get_workflows(db: Session, skip: int = 0, limit: int = 100):
    return workflow_crud.get_workflows(db, skip, limit)

def create_workflow(db: Session, workflow: WorkflowCreate):
    return workflow_crud.create_workflow(db, workflow)

def update_workflow(db: Session, workflow_id: int, workflow: WorkflowUpdate):
    # 修复：确保参数类型正确传递
    return workflow_crud.update_workflow(db, workflow_id, workflow)

def delete_workflow(db: Session, workflow_id: int):
    return workflow_crud.delete_workflow(db, workflow_id)