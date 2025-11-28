import secrets
import hashlib
from typing import List, Optional
from app.models.models import App
from app.schemas.app_schema import AppCreate, AppUpdate
from django.db import transaction
from asgiref.sync import sync_to_async

class AppService:
    @staticmethod
    def generate_app_key() -> str:
        """生成应用Key"""
        return f"ak_{secrets.token_hex(16)}"
    
    @staticmethod
    def generate_app_secret() -> str:
        """生成应用密钥"""
        return f"as_{secrets.token_hex(32)}"
    
    @staticmethod
    @sync_to_async
    @transaction.atomic
    def create_app(app_data: AppCreate) -> App:
        """创建应用"""
        app = App(
            app_name=app_data.app_name,
            description=app_data.description,
            app_key=AppService.generate_app_key(),
            app_secret=AppService.generate_app_secret(),
            status=1
        )
        app.save()
        return app
    
    @staticmethod
    def get_app_by_id(app_id: int, status: int = 1) -> Optional[App]:
        """根据ID获取应用"""
        try:
            return App.objects.get(id=app_id, status=status)
        except App.DoesNotExist:
            return None
    
    @staticmethod
    def get_app_by_key(app_key: str) -> Optional[App]:
        """根据app_key获取应用"""
        try:
            return App.objects.get(app_key=app_key)
        except App.DoesNotExist:
            return None
    
    @staticmethod
    def get_apps(page: int = 1, page_size: int = 20) -> tuple[List[App], int]:
        """获取应用列表"""
        offset = (page - 1) * page_size
        apps = App.objects.filter(status=1).order_by('-created_at')[offset:offset + page_size]
        total = App.objects.filter(status=1).count()
        return list(apps), total
    
    @staticmethod
    @sync_to_async
    @transaction.atomic
    def update_app(app_id: int, app_data: AppUpdate) -> Optional[App]:
        """更新应用"""
        # 直接在同步环境中查询，不通过异步方法
        try:
            app = App.objects.get(id=app_id, status=1)
        except App.DoesNotExist:
            return None
        
        if app_data.app_name is not None:
            app.app_name = app_data.app_name
        if app_data.description is not None:
            app.description = app_data.description
        if app_data.status is not None:
            app.status = app_data.status
        
        app.save()
        return app
    
    @staticmethod
    @sync_to_async
    @transaction.atomic
    def delete_app(app_id: int) -> bool:
        """删除应用(软删除)"""
        app = AppService.get_app_by_id(app_id, status=1)
        if not app:
            return False
        
        app.status = 0
        app.save()
        return True