from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.services.model_service import ModelService
from typing import Optional

router = APIRouter(prefix="/models", tags=["models"])

class ModelRequest(BaseModel):
    prompt: str
    max_tokens: Optional[int] = 1024
    temperature: Optional[float] = 0.8

class ModelResponse(BaseModel):
    success: bool
    data: Optional[dict] = None
    error: Optional[str] = None

@router.post("/qwen-plus", response_model=ModelResponse)
async def call_qwen_plus(request: ModelRequest):
    service = ModelService()
    result = await service.process_with_qwen_plus(
        prompt=request.prompt,
        max_tokens=request.max_tokens,
        temperature=request.temperature
    )
    return ModelResponse(**result)