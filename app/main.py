import sys
import os

# Add the parent directory to the Python path so 'app' module can be imported
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes import workflows, models
from app.core.database import engine, Base
import app.models.workflow

# Force import of all models to ensure they are all registered before creating tables
print("Importing models...")
print("Creating database tables...")
Base.metadata.create_all(bind=engine)
print("Database tables created.")
tables = Base.metadata.tables.keys()
print(f"Tables that should be created: {list(tables)}")

app = FastAPI(title="Dify-like System")

# 添加CORS中间件以允许前端访问
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 在生产环境中应该指定具体的域名
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 确保重定向行为符合预期
app.include_router(workflows.router, prefix="/api/v1")
app.include_router(models.router, prefix="/api/v1")

@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/health")
async def health_check():
    return {"status": "healthy"}

@app.get("/debug/db-info")
def debug_db_info():
    """Debug endpoint to check database status"""
    from app.core.database import SessionLocal
    db = SessionLocal()
    try:
        # Check if tables exist
        from sqlalchemy import text
        result = db.execute(text("SELECT name FROM sqlite_master WHERE type='table'")).fetchall()
        tables = [row[0] for row in result]
        
        # Check workflow count
        workflow_count = 0
        if 'workflows' in tables:
            result = db.execute(text("SELECT COUNT(*) FROM workflows")).fetchone()
            workflow_count = result[0] if result else 0
            
        return {
            "tables": tables,
            "workflow_count": workflow_count
        }
    finally:
        db.close()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)