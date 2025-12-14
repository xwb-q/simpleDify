from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from app import crud, schemas
from app.core.database import get_db
from app.services.workflow_execution_service import WorkflowExecutionService

router = APIRouter(prefix="/workflows", tags=["workflows"])

@router.get("/", response_model=List[schemas.Workflow])
def read_workflows(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    workflows = crud.workflow_crud.get_workflows(db, skip=skip, limit=limit)
    print(f"Fetched {len(workflows)} workflows")  # 添加调试日志
    return workflows

@router.get("/{workflow_id}", response_model=schemas.Workflow)
def read_workflow(workflow_id: int, db: Session = Depends(get_db)):
    db_workflow = crud.workflow_crud.get_workflow(db, workflow_id=workflow_id)
    if db_workflow is None:
        raise HTTPException(status_code=404, detail="Workflow not found")
    return db_workflow

@router.post("/", response_model=schemas.Workflow)
def create_workflow(workflow: schemas.WorkflowCreate, db: Session = Depends(get_db)):
    print(f"Creating workflow with data: {workflow}")  # 添加调试日志
    return crud.workflow_crud.create_workflow(db=db, workflow=workflow)

@router.put("/{workflow_id}", response_model=schemas.Workflow)
def update_workflow_route(workflow_id: int, workflow: schemas.WorkflowUpdate, db: Session = Depends(get_db)):
    # 修复：将参数类型从 WorkflowCreate 改为 WorkflowUpdate
    db_workflow = crud.workflow_crud.update_workflow(db, workflow_id, workflow)
    if db_workflow is None:
        raise HTTPException(status_code=404, detail="Workflow not found")
    return db_workflow

@router.delete("/{workflow_id}")
def delete_workflow_route(workflow_id: int, db: Session = Depends(get_db)):
    db_workflow = crud.workflow_crud.delete_workflow(db, workflow_id)
    if db_workflow is None:
        raise HTTPException(status_code=404, detail="Workflow not found")
    return {"message": "Workflow deleted successfully"}

@router.post("/{workflow_id}/execute")
async def execute_workflow(workflow_id: int, input_data: Optional[str] = None, db: Session = Depends(get_db)):
    service = WorkflowExecutionService(db)
    try:
        result = await service.execute_workflow(workflow_id, input_data)
        return result
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
