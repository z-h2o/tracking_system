from typing import List, Optional, Dict, Any
from datetime import datetime
from app.models.models import TrackingEvent
from app.schemas.event_schema import EventCreate
from django.db import transaction
from django.db.models import Count, Q
from asgiref.sync import sync_to_async

class TrackingService:
    @staticmethod
    @sync_to_async
    @transaction.atomic
    def create_event(app_key: str, event_data: EventCreate, ip: str = None, user_agent: str = None) -> TrackingEvent:
        """创建单个埋点事件"""
        event = TrackingEvent(
            app_key=app_key,
            user_id=event_data.user_id,
            device_id=event_data.device_id,
            event_type=event_data.event_type,
            event_name=event_data.event_name,
            properties=event_data.properties,
            page_url=event_data.page_url,
            referrer=event_data.referrer,
            platform=event_data.platform,
            os_version=event_data.os_version,
            app_version=event_data.app_version,
            ip=ip,
            user_agent=user_agent,
            event_time=event_data.event_time
        )
        event.save()
        return event
    
    @staticmethod
    @sync_to_async
    @transaction.atomic
    def batch_create_events(app_key: str, events_data: List[EventCreate], ip: str = None, user_agent: str = None) -> tuple[int, int]:
        """批量创建埋点事件"""
        success_count = 0
        failed_count = 0
        
        for event_data in events_data:
            try:
                TrackingService.create_event(app_key, event_data, ip, user_agent)
                success_count += 1
            except Exception as e:
                failed_count += 1
                print(f"Failed to create event: {e}")
        
        return success_count, failed_count
    
    @staticmethod
    @sync_to_async
    def query_events(
        app_key: Optional[str] = None,
        event_type: Optional[str] = None,
        user_id: Optional[str] = None,
        device_id: Optional[str] = None,
        start_time: Optional[datetime] = None,
        end_time: Optional[datetime] = None,
        page: int = 1,
        page_size: int = 20
    ) -> tuple[List[TrackingEvent], int]:
        """查询埋点事件"""
        query = Q()
        
        if app_key:
            query &= Q(app_key=app_key)
        if event_type:
            query &= Q(event_type=event_type)
        if user_id:
            query &= Q(user_id=user_id)
        if device_id:
            query &= Q(device_id=device_id)
        if start_time:
            query &= Q(event_time__gte=start_time)
        if end_time:
            query &= Q(event_time__lte=end_time)
        
        offset = (page - 1) * page_size
        events = TrackingEvent.objects.filter(query).order_by('-event_time')[offset:offset + page_size]
        total = TrackingEvent.objects.filter(query).count()
        
        return list(events), total
    
    @staticmethod
    @sync_to_async
    def get_event_statistics(
        app_key: str,
        start_time: Optional[datetime] = None,
        end_time: Optional[datetime] = None,
        group_by: str = 'event_type'
    ) -> List[Dict[str, Any]]:
        """获取事件统计"""
        query = Q(app_key=app_key)
        
        if start_time:
            query &= Q(event_time__gte=start_time)
        if end_time:
            query &= Q(event_time__lte=end_time)
        
        if group_by == 'event_type':
            stats = TrackingEvent.objects.filter(query).values('event_type').annotate(
                count=Count('id'),
                unique_users=Count('user_id', distinct=True),
                unique_devices=Count('device_id', distinct=True)
            ).order_by('-count')
        else:
            stats = TrackingEvent.objects.filter(query).values(group_by).annotate(
                count=Count('id')
            ).order_by('-count')
        
        return list(stats)