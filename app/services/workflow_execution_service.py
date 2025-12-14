from sqlalchemy.orm import Session
from app.models.workflow import Workflow, Task
from app.services.model_service import ModelService
import json
import logging

logger = logging.getLogger(__name__)

class WorkflowExecutionService:
    def __init__(self, db: Session):
        self.db = db
        self.model_service = ModelService()
    
    async def execute_workflow(self, workflow_id: int, input_data: str = None):
        """
        执行工作流
        :param workflow_id: 工作流ID
        :param input_data: 用户输入数据（可选）
        :return: 执行结果
        """
        workflow = self.db.query(Workflow).filter(Workflow.id == workflow_id).first()
        if not workflow:
            raise ValueError(f"Workflow with id {workflow_id} not found")
        
        # 解析工作流描述中的节点信息，查找Start节点的输入
        start_node_input = input_data  # 默认使用传入的input_data
        if not input_data and workflow.description:
            try:
                metadata = json.loads(workflow.description)
                nodes = metadata.get("nodes", [])
                # 查找Start节点并获取其输入值
                for node in nodes:
                    if node.get("type") == "startNode":
                        start_node_input = node.get("data", {}).get("inputValue")
                        break
            except json.JSONDecodeError:
                logger.warning(f"Failed to parse workflow metadata for workflow {workflow_id}")
        
        results = []
        # 按顺序执行任务
        tasks = sorted(workflow.tasks, key=lambda x: x.order)
        
        # 存储上一个任务的输出，用于传递给下一个任务
        # 如果Start节点有输入，则将其作为初始输入
        previous_output = start_node_input
        
        for task in tasks:
            try:
                result = await self.execute_task(task, previous_output)
                results.append({
                    "task_id": task.id,
                    "task_name": task.name,
                    "result": result
                })
                # 将当前任务的结果作为下一个任务的输入
                # 只有成功的结果才传递给下一个任务
                if isinstance(result, dict) and result.get("success"):
                    previous_output = result.get("data")
                elif result is not None:
                    previous_output = result
            except Exception as e:
                logger.error(f"Error executing task {task.name}: {str(e)}")
                results.append({
                    "task_id": task.id,
                    "task_name": task.name,
                    "error": str(e)
                })
                # 根据需求决定是否继续执行后续任务
                break
        
        return {
            "workflow_id": workflow_id,
            "workflow_name": workflow.name,
            "results": results,
            "final_output": previous_output
        }
    
    async def execute_task(self, task: Task, input_data=None):
        """
        执行单个任务
        :param task: 任务对象
        :param input_data: 上一个任务的输出作为输入
        :return: 任务执行结果
        """
        if task.type == "llm":
            # 解析任务配置
            config = {}
            if task.config:
                try:
                    config = json.loads(task.config)
                except json.JSONDecodeError:
                    logger.warning(f"Invalid config for task {task.name}")
            
            # 获取节点数据中的自定义提示或使用默认提示
            node_data = config.get("node_data", {})
            custom_prompt = node_data.get("prompt", "")
            
            # 如果有自定义提示，则使用它，否则构建默认提示
            if custom_prompt:
                # 如果有输入数据，将其附加到自定义提示中
                if input_data:
                    # 如果输入数据是字典且包含特定字段，则提取内容
                    if isinstance(input_data, dict):
                        if "choices" in input_data and input_data["choices"]:
                            # OpenAI风格的响应
                            content = input_data["choices"][0].get("message", {}).get("content", str(input_data))
                        elif "data" in input_data:
                            # 我们的模型服务响应
                            content = input_data["data"]
                        else:
                            content = str(input_data)
                    else:
                        content = str(input_data)
                        
                    prompt = f"{custom_prompt}\n\nInput data: {content}"
                else:
                    prompt = custom_prompt
            else:
                # 没有自定义提示时使用默认行为
                node_label = node_data.get("label", "")
                base_prompt = f"Process node: {node_label}" if node_label else "Process the following input:"
                
                # 如果有输入数据，则构建更丰富的提示
                if input_data:
                    # 如果输入数据是字典且包含特定字段，则提取内容
                    if isinstance(input_data, dict):
                        if "choices" in input_data and input_data["choices"]:
                            # OpenAI风格的响应
                            content = input_data["choices"][0].get("message", {}).get("content", str(input_data))
                        elif "data" in input_data:
                            # 我们的模型服务响应
                            content = input_data["data"]
                        else:
                            content = str(input_data)
                    else:
                        content = str(input_data)
                        
                    prompt = f"{base_prompt}\n\nInput data: {content}\n\nPlease process this input according to your instructions."
                else:
                    prompt = base_prompt
            
            # 调用大模型，使用专门的工作流系统提示
            result = await self.model_service.process_with_qwen_plus(
                prompt=prompt,
                system_prompt_path="app/sysprompt/workflow_prompt.md",
                max_tokens=config.get("max_tokens", 1024),
                temperature=config.get("temperature", 0.8)
            )
            return result
        else:
            # 其他类型的任务可以在这里添加
            return {"message": f"Task type {task.type} not implemented yet"}