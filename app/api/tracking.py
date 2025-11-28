from fastapi import APIRouter, status, Depends, Request, BackgroundTasks
from typing import Optional
from datetime import datetime
from app.schemas.event_schema import EventCreate, EventBatchCreate, EventResponse
from app.schemas.response_schema import ResponseModel
from app.services.tracking_service import TrackingService
from app.middleware.auth import verify_app_key
from app.utils.response_utils import success_response, error_response

router = APIRouter(prefix="/api/v1", tags=["埋点数据"])

def get_client_info(request: Request) -> tuple[str, str]:
    """获取客户端信息"""
    ip = request.client.host if request.client else None
    user_agent = request.headers.get("user-agent", "")
    return ip, user_agent

async def save_event_background(app_key: str, event_data: EventCreate, ip: str, user_agent: str):
    """后台任务:保存事件"""
    try:
        await TrackingService.create_event(app_key, event_data, ip, user_agent)
    except Exception as e:
        print(f"Background task failed: {e}")

@router.post("/track", response_model=ResponseModel, status_code=status.HTTP_201_CREATED)
async def track_event(
    event_data: EventCreate,
    background_tasks: BackgroundTasks,
    request: Request,
    app_key: str = Depends(verify_app_key)
):
    """单个事件上报"""
    try:
        ip, user_agent = get_client_info(request)
        
        # 使用后台任务异步保存
        event = await TrackingService.create_event(app_key, event_data, ip, user_agent)
        
        return success_response({
            "event_id": event.id
        })
    except Exception as e:
        return error_response(f"Failed to track event: {str(e)}")

@router.post("/track/batch", response_model=ResponseModel, status_code=status.HTTP_201_CREATED)
async def track_batch_events(
    batch_data: EventBatchCreate,
    request: Request,
    app_key: str = Depends(verify_app_key)
):
    """批量事件上报"""
    try:
        ip, user_agent = get_client_info(request)
        success_count, failed_count = await TrackingService.batch_create_events(
            app_key, batch_data.events, ip, user_agent
        )
        
        return success_response({
            "success_count": success_count,
            "failed_count": failed_count
        })
    except Exception as e:
        return error_response(f"Failed to track batch events: {str(e)}")

@router.get("/events", response_model=ResponseModel)
async def query_events(
    app_key: Optional[str] = None,
    event_type: Optional[str] = None,
    user_id: Optional[str] = None,
    device_id: Optional[str] = None,
    start_time: Optional[datetime] = None,
    end_time: Optional[datetime] = None,
    page: int = 1,
    page_size: int = 20
):
    """查询事件列表"""
    try:
        events, total = await TrackingService.query_events(
            app_key=app_key,
            event_type=event_type,
            user_id=user_id,
            device_id=device_id,
            start_time=start_time,
            end_time=end_time,
            page=page,
            page_size=page_size
        )
        
        return success_response({
            "total": total,
            "page": page,
            "page_size": page_size,
            "events": [EventResponse.model_validate(event).model_dump() for event in events]
        })
    except Exception as e:
        return error_response(f"Failed to query events: {str(e)}")

@router.get("/events/stats", response_model=ResponseModel)
async def get_event_statistics(
    app_key: str,
    start_time: Optional[datetime] = None,
    end_time: Optional[datetime] = None,
    group_by: str = "event_type"
):
    """获取事件统计"""
    try:
        stats = await TrackingService.get_event_statistics(
            app_key=app_key,
            start_time=start_time,
            end_time=end_time,
            group_by=group_by
        )
        
        return success_response({"statistics": stats})
    except Exception as e:
        return error_response(f"Failed to get statistics: {str(e)}")
