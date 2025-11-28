from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class AppCreate(BaseModel):
    app_name: str = Field(..., min_length=1, max_length=100, description="应用名称")
    description: Optional[str] = Field(None, description="应用描述")

class AppUpdate(BaseModel):
    app_name: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = None
    status: Optional[int] = Field(None, ge=0, le=1)

class AppResponse(BaseModel):
    id: int
    app_name: str
    app_key: str
    app_secret: str
    description: Optional[str]
    status: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True