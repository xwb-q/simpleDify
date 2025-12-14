from sqlalchemy.orm import Session
from app.models.workflow import Workflow, Task
from app.schemas.workflow import WorkflowCreate, WorkflowUpdate
import json
import logging

logger = logging.getLogger(__name__)

def get_workflows(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Workflow).offset(skip).limit(limit).all()

def get_workflow(db: Session, workflow_id: int):
    return db.query(Workflow).filter(Workflow.id == workflow_id).first()

def create_workflow(db: Session, workflow: WorkflowCreate):
    # 解析描述中的节点信息
    nodes_data = []
    if workflow.description:
        try:
            metadata = json.loads(workflow.description)
            nodes_data = metadata.get("nodes", [])
        except json.JSONDecodeError:
            print("Failed to parse workflow metadata")

    db_workflow = Workflow(
        name=workflow.name,
        description=workflow.description
    )
    db.add(db_workflow)
    db.commit()
    print("Committed transaction")
    print(f"Workflow ID after commit: {getattr(db_workflow, 'id', 'No ID assigned')}")
    
    # 创建任务（基于节点数据）
    for i, node in enumerate(nodes_data):
        # 只为模型节点创建任务
        if node.get("type") == "modelNode":
            # 构建更丰富的任务配置
            task_config = {
                "prompt": node.get("data", {}).get("prompt", f"Process node: {node.get('data', {}).get('label', '')}"),
                "node_id": node.get("id"),
                "node_data": node.get("data", {}),
                "position": node.get("position", {})
            }
            
            task = Task(
                name=node.get("data", {}).get("label", f"Task {i+1}"),
                description=f"Task for node {node.get('id')}",
                workflow_id=db_workflow.id,
                type="llm",
                order=i,
                config=json.dumps(task_config)
            )
            db.add(task)
    
    db.commit()
    
    # 直接返回创建的工作流对象
    return db_workflow

def update_workflow(db: Session, workflow_id: int, workflow: WorkflowUpdate):
    db_workflow = db.query(Workflow).filter(Workflow.id == workflow_id).first()
    if db_workflow:
        # 更新基本信息
        db_workflow.name = workflow.name
        db_workflow.description = workflow.description
        
        # 解析描述中的节点信息
        nodes_data = []
        if workflow.description:
            try:
                metadata = json.loads(workflow.description)
                nodes_data = metadata.get("nodes", [])
            except json.JSONDecodeError:
                print("Failed to parse workflow metadata")
        
        # 删除现有任务
        db.query(Task).filter(Task.workflow_id == workflow_id).delete()
        
        # 重新创建任务（基于节点数据）
        for i, node in enumerate(nodes_data):
            # 只为模型节点创建任务
            if node.get("type") == "modelNode":
                # 构建更丰富的任务配置
                task_config = {
                    "prompt": node.get("data", {}).get("prompt", f"Process node: {node.get('data', {}).get('label', '')}"),
                    "node_id": node.get("id"),
                    "node_data": node.get("data", {}),
                    "position": node.get("position", {})
                }
                
                task = Task(
                    name=node.get("data", {}).get("label", f"Task {i+1}"),
                    description=f"Task for node {node.get('id')}",
                    workflow_id=workflow_id,
                    type="llm",
                    order=i,
                    config=json.dumps(task_config)
                )
                db.add(task)
        
        db.commit()
        print(f"Successfully updated workflow {workflow_id}")
    else:
        print(f"Workflow with id {workflow_id} not found for update")
    return db_workflow

def delete_workflow(db: Session, workflow_id: int):
    db_workflow = db.query(Workflow).filter(Workflow.id == workflow_id).first()
    if db_workflow:
        db.delete(db_workflow)
        db.commit()
        print(f"Successfully deleted workflow {workflow_id}")
    else:
        print(f"Workflow with id {workflow_id} not found for deletion")
    return db_workflow