from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy import text
from app.core.database import Base
from datetime import datetime

class Workflow(Base):
    __tablename__ = "workflows"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String, index=True, nullable=False)
    description = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # 关联任务
    tasks = relationship("Task", back_populates="workflow", cascade="all, delete-orphan")
    
    # 确保SQLite中的AUTOINCREMENT
    __table_args__ = {'sqlite_autoincrement': True}

class Task(Base):
    __tablename__ = "tasks"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String, index=True, nullable=False)
    description = Column(Text, nullable=True)
    workflow_id = Column(Integer, ForeignKey("workflows.id"), nullable=False)
    # 任务类型，如 'llm'(大模型调用), 'code'(代码执行), 'http'(HTTP请求)等
    type = Column(String, default="llm")
    # 任务配置参数
    config = Column(Text, nullable=True)
    # 执行顺序
    order = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # 关联工作流
    workflow = relationship("Workflow", back_populates="tasks")
    
    # 确保SQLite中的AUTOINCREMENT
    __table_args__ = {'sqlite_autoincrement': True}