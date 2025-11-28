from pydantic import BaseModel, Field
from typing import Optional, Dict, Any, List
from datetime import datetime

class EventCreate(BaseModel):
    event_type: str = Field(..., min_length=1, max_length=50, description="事件类型")
    event_name: str = Field(..., min_length=1, max_length=100, description="事件名称")
    user_id: Optional[str] = Field(None, max_length=64, description="用户ID")
    device_id: str = Field(..., min_length=1, max_length=128, description="设备ID")
    properties: Optional[Dict[str, Any]] = Field(None, description="事件属性")
    page_url: Optional[str] = Field(None, max_length=500, description="页面URL")
    referrer: Optional[str] = Field(None, max_length=500, description="来源页面")
    platform: Optional[str] = Field(None, max_length=20, description="平台")
    os_version: Optional[str] = Field(None, max_length=50, description="系统版本")
    app_version: Optional[str] = Field(None, max_length=50, description="应用版本")
    event_time: datetime = Field(..., description="事件时间")

class EventBatchCreate(BaseModel):
    events: List[EventCreate] = Field(..., min_items=1, max_items=100, description="事件列表")

class EventQuery(BaseModel):
    app_key: Optional[str] = None
    event_type: Optional[str] = None
    user_id: Optional[str] = None
    device_id: Optional[str] = None
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    page: int = Field(1, ge=1)
    page_size: int = Field(20, ge=1, le=100)

class EventResponse(BaseModel):
    id: int
    app_key: str
    user_id: Optional[str]
    device_id: str
    event_type: str
    event_name: str
    properties: Optional[Dict[str, Any]]
    event_time: datetime
    created_at: datetime

    class Config:
        from_attributes = True